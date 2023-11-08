from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
import datetime

from .models import Group, Student, Attendance, AttendanceStatus

# Create your views here.

TODAYS_DATE = timezone.now().date()


@login_required(login_url='/login/')
def home(request):
    groups = Group.objects.all()
    context = {'groups': groups, 'todays_date': TODAYS_DATE}
    return render(request, 'home.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if user exists
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            redirect('home')
            return render(request, 'home.html')
        else:
            messages.success(request, ('Error logging in - please try again...'))
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    redirect('home')
    return render(request, 'home.html')


@login_required
def students_page(request, group_name):
    have_taken_an_attendance = False
    teacher = request.user
    group = Group.objects.get(name=group_name)
    students = Student.objects.filter(group=group)
    if Attendance.objects.filter(teacher=teacher, group=group, date=TODAYS_DATE).exists():
        have_taken_an_attendance = True

    context = {'todays_date': TODAYS_DATE, 'group': group, 'students': students,
               'have_taken_an_attendance': have_taken_an_attendance}
    return render(request, 'students.html', context)


@login_required(login_url='/login/')
def take_an_attendance(request, group_name):
    teacher = request.user
    group = Group.objects.get(name=group_name)
    students = Student.objects.filter(group=group)
    context = {'todays_date': TODAYS_DATE, 'group': group, 'students': students}

    if request.method == 'POST':
        attendance, created = Attendance.objects.get_or_create(
            teacher=teacher,
            group=group,
            date=TODAYS_DATE
        )
        for student in students:
            present = request.POST.get(str(student.id))
            attendance_status, created = AttendanceStatus.objects.get_or_create(
                attendance=attendance,
                student=student
            )
            attendance_status.present = present == 'on'
            attendance_status.save()

        return redirect('list_students', group_name=group_name)

    return render(request, 'take_an_attendance.html', context)


@login_required(login_url='/login/')
def update_attendance(request, group_name):
    teacher = request.user
    group = Group.objects.get(name=group_name)
    students = Student.objects.filter(group=group)

    attendance, created = Attendance.objects.get_or_create(
        teacher=teacher,
        group=group,
        date=TODAYS_DATE
    )

    attendance_status = AttendanceStatus.objects.filter(attendance=attendance)
    student_attendance = {}
    for status in attendance_status:
        student_attendance[status.student.id] = status.present
    context = {'todays_date': TODAYS_DATE, 'group': group, 'students': students,
               'student_attendance': student_attendance}

    if request.method == 'POST':
        for student in students:
            present = request.POST.get(str(student.id))
            attendance_status, created = AttendanceStatus.objects.get_or_create(
                attendance=attendance,
                student=student
            )
            attendance_status.present = present == 'on'
            attendance_status.save()

        return redirect('list_students', group_name=group_name)

    return render(request, 'update_attendance.html', context)


def attendance_history(request, group_name):
    group = Group.objects.get(name=group_name)
    dates = Attendance.objects.filter(group=group).values_list('date', flat=True).distinct()
    print(dates)
    context = {'group': group, 'dates': dates}
    return render(request, 'attendance_history.html', context)


def view_attendance(request, group_name, date):
    teacher = request.user
    group = Group.objects.get(name=group_name)
    selected_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()  # Convert date string to a date object
    attendance = Attendance.objects.filter(group=group, date=selected_date, teacher=teacher)
    attendance = attendance[0].attendancestatus_set.all()
    context = {'group': group, 'date': selected_date, 'attendance': attendance}
    return render(request, 'view_attendance.html', context)
