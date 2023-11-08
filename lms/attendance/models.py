from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=20, unique=True)
    __str__ = lambda self: self.name

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.FloatField(null=True, blank=True)
    __str__ = lambda self: f'{self.first_name} {self.last_name}'

    # @property
    # def attendence_percentage(self):
    #     pass
    #
    # def save(self, *args, **kwargs):
    #     self.status = self.attendence_percentage
    #     super().save(*args, **kwargs)

class Attendance(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    students = models.ManyToManyField(Student, through='AttendanceStatus')

    def __str__(self):
        return f'{self.group} - {self.date}'


class AttendanceStatus(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    present = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.student} - {self.present}'
