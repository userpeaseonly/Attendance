from django.contrib import admin
from .models import Attendance, Student, Group, AttendanceStatus

# Register your models here.

admin.site.register(Attendance)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(AttendanceStatus)