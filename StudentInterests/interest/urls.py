from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_login, name='login'),
    path('students/list', views.student_list, name='student-list'),
    path('students/create/', views.student_create, name='student-create'),
    path('students/dashboard/', views.student_dashboard, name='student-dashboard'),
    path('students/<int:pk>/', views.student_detail, name='student-detail'),
    path('students/<int:pk>/update/', views.student_update, name='student-update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student-delete'),
    path('students/<int:pk>/activity/', views.activity_log, name='activity-log'),
    path('log-activity/', views.log_activity, name='log_activity'),
    path('logout/', views.logout_view, name='logout')
]


