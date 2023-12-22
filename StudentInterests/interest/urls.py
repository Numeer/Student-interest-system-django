from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.student_list, name='student-list'),
    path('students/create/', views.student_create, name='student-create'),
    path('students/<int:pk>/', views.student_detail, name='student-detail'),
    path('students/<int:pk>/update/', views.student_update, name='student-update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student-delete'),
    path('students/<int:pk>/activity/', views.activity_log, name='activity-log'),
]


#  INTEREST_CHOICES = (
#         ('Technology', 'Technology'),
#         ('Science', 'Science'),
#         ('Arts', 'Arts'),
#         ('Music', 'Music'),
#         ('Movies', 'Movies'),
#         ('Sports', 'Sports'),
#         ('Books', 'Books'),
#         ('Travel', 'Travel'),
#         ('Cooking', 'Cooking'),
#         ('Fashion', 'Fashion'),
#         ('Health', 'Health'),
#         ('Fitness', 'Fitness'),
#         ('Gaming', 'Gaming'),
#         ('Photography', 'Photography'),
#         ('Dance', 'Dance'),
#         ('Animals', 'Animals'),
#         ('Nature', 'Nature'),
#         ('History', 'History'),
#         ('Politics', 'Politics'),
#         ('Programming', 'Programming'),
#         ('Business', 'Business'),
#         ('Languages', 'Languages'),
#         ('Education', 'Education'),
#         ('Design', 'Design'),
#         ('Psychology', 'Psychology'),
#         ('Sustainability', 'Sustainability'),
#         ('Philosophy', 'Philosophy'),
#         ('Crafts', 'Crafts'),
#         ('DIY', 'DIY'),
#         ('Social Media', 'Social Media'),
#         ('Writing', 'Writing'),
#         ('Other', 'Other'),
#     )