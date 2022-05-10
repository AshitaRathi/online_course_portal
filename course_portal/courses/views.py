from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
# from django.core.files import File
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import register

@register.filter(name='dict_key')
def dict_key(d, k):
    '''Returns the given key from a dictionary.'''
    return d[k]

def register(response):
    if response.method == "POST":
        form = CustomUserCreationForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/login")
    else:
        form = CustomUserCreationForm()
        return render(response, "registration/register.html", {"form":form})

def login_user(request):
    logout(request)
    email = password = ''
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index/')
    return render(request,'registration/login.html')

@login_required(login_url='/login/')
def index(request):
    course = Course.objects.all()
    user_type = request.user.user_type
    page = request.GET.get('page', 1)
    paginator = Paginator(course, 7)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'pages/index.html',{"course":page_obj,"user_type":user_type})

def selected_course(request,pk):
    course = Course.objects.get(pk=pk)
    user_id = request.user.id
    user_type = request.user.user_type
    comments = Comment.objects.filter(course_id=pk)
    try:
        enroll = Enrollment.objects.get(user_id=user_id,course_id=course.id)
        return render(request, 'pages/enrolled_course.html',{"course":course,"user_type":user_type,"comments":comments})
    except Enrollment.DoesNotExist:
        return render(request, 'pages/course.html',{"course":course,"user_type":user_type,"comments":comments})
    
def user_enrollment(request,pk):
    user_id = request.user.id
    user_type = request.user.user_type
    course = Course.objects.get(pk=pk)
    comments = Comment.objects.filter(course_id=pk)        
    try:
        enroll = Enrollment.objects.get(user_id=user_id,course_id=course.id)
        print(enroll)
        return render(request, 'pages/enrolled_course.html',{"course":course,"user_type":user_type,"comments":comments})
    except Enrollment.DoesNotExist:
        Enrollment.objects.create(user_id=user_id, is_enrolled=True, course_id=course.id)
        return render(request, 'pages/enrolled_course.html',{"course":course,"user_type":user_type,"comments":comments})

def your_courses(request):
    user_id = request.user.id
    user_type = request.user.user_type
    course = Course.objects.filter(user_id=user_id)
    return render(request, 'pages/your_courses.html',{"course":course,"user_type":user_type})

def student_enrolled_courses(request):
    user_id = request.user.id
    user_type = request.user.user_type
    enrolled = Enrollment.objects.filter(user_id=user_id).values_list('course_id')
    course=[]
    for i in enrolled :
        c = Course.objects.get(pk=i[0])
        course.append(c)
    return render(request, 'pages/student_enrolled_courses.html',{"course":course,"user_type":user_type})

def add_course(request):
    user_type = request.user.user_type
    form= CourseForm(request.POST,request.FILES)
    if form.is_valid():
        f = form.save(commit=False)
        f.user_id=request.user.id
        f.save()
        return redirect("/index")
    context= {'form': form,"user_type":user_type }
        
    return render(request, 'pages/add_course.html', context)

    
def course_update(request, pk):
    user_type = request.user.user_type
    course = Course.objects.get(id=pk)
    print(course)
    if request.method == 'POST':
        form = CourseForm(request.POST,request.FILES,instance=course)
        if form.is_valid():
            form.save()
            return redirect('/index')
    else:
        form = CourseForm(instance=course)

    return render(request,'pages/course_update.html',{'form': form,"user_type":user_type})

def delete_course(request, pk):
    obj = Course.objects.get(id=pk)
    obj.delete()
    return HttpResponseRedirect("/index")

def comment(request, pk):
    if request.method == 'POST':
        cf = CommentForm(request.POST or None)
        if cf.is_valid():
            username = request.POST.get('username')
            description = request.POST.get('description')
            comment = Comment.objects.create(user_id = request.user.id, username=username,description = description,course_id=pk)
            comment.save()
            return redirect('user_enrollment', pk=pk)
    else:
        cf = CommentForm()
        
    context ={
    'comment_form':cf,
    }
    return render(request, 'pages/comment.html', context)


class SearchResultsView(ListView):
    model = Course
    template_name = "pages/search_course.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Course.objects.filter(
            Q(course_name__icontains=query) | Q(course_type__icontains=query)
        )
        return object_list