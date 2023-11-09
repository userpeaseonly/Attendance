from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    @property
    def attendance_percentage(self):
        if self.pk:  # Check if the student has been saved
            total_attendances = self.attendancestatus_set.count()
            present_attendances = self.attendancestatus_set.filter(present=True).count()

            if total_attendances > 0:
                percentage = (present_attendances / total_attendances) * 100
                return round(percentage, 2)
            else:
                return 0.0
        else:
            return 0.0

    def save(self, *args, **kwargs):
        self.status = self.attendance_percentage
        super().save(*args, **kwargs)


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


@receiver(post_save, sender=AttendanceStatus)
def update_student_status(sender, instance, **kwargs):
    student = instance.student
    student.status = student.attendance_percentage
    student.save()