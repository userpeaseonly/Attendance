from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('list_students/<str:group_name>', views.students_page, name='list_students'),
    path('list_students/take_an_attendance/<str:group_name>', views.take_an_attendance, name='take_an_attendance'),
    path('list_students/update_attendance/<str:group_name>', views.update_attendance, name='update_attendance'),
    path('list_students/<str:group_name>/history/', views.attendance_history, name='attendance_history'),
    path('list_students/<str:group_name>/history/<str:date>/', views.view_attendance, name='view_attendance'),
    path('list_students/<str:group_name>/<int:student_id>/', views.student_detail, name='student_detail'),
]
