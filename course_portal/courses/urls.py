from courses.views import *
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_user,name="login"),
    path('index/', index, name='index'),
    path('add_course/', add_course, name='add_course'),
    path('course_update/<int:pk>/', course_update, name='course_update'),
    path('delete_course/<int:pk>/', delete_course, name='delete_course'),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path('your_courses/', your_courses, name='your_courses'),
    path('student_enrolled_courses/', student_enrolled_courses, name='student_enrolled_courses'),
    path('course/<int:pk>/', selected_course, name='selected_course'),
    path('enroll/<int:pk>/', user_enrollment, name='user_enrollment'),
    path('comment/<int:pk>/', comment, name='comment'),
    path('', include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)