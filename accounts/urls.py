from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('students-viewset', views.StudentViewSet)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('api/hello/', views.hello_api, name='hello_api'),
    path('api/students/', views.student_list, name='student_list'),
    path('api/students/<int:pk>/', views.student_detail, name='student_detail'),
    path('api/', include(router.urls)),
    path('students/add/', views.add_student, name='add_student'),
    path(
    'students/add-multiple/',
    views.add_multiple_students,
    name='add_multiple_students'
),
    path(
    'students/',
    views.student_list_page,
    name='student_list_page'
),
]