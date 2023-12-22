from datetime import date, timedelta
from django.forms import model_to_dict
from django.http import JsonResponse
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, redirect, render
from interest.StudentForm import StudentForm
from django.db.models import Count
from interest.models import ActivityLog, Interest, Student
from django.db.models.functions import ExtractYear
from django.db.models import F, ExpressionWrapper, fields
from django.db.models import Value, DateField
    
# Views for CRUD operations on Student model
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student-detail', pk=form.instance.pk)
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'student_detail.html', {'student': student})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student-list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_update.html', {'form': form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student-list')
    return render(request, 'student_confirm_delete.html', {'student': student})

def activity_log(request, pk):
    student = get_object_or_404(Student, pk=pk)
    activity_logs = ActivityLog.objects.filter(user=student).values()
    return JsonResponse(list(activity_logs), safe=False)


def student_dashboard(request):
    top_interests = (
        Interest.objects.filter(student__isnull=False)
        .values('name')
        .annotate(count=Count('student__interest'))
        .order_by('-count')[:5]
    )

    bottom_interests = (
        Interest.objects.filter(student__isnull=False)
        .values('name')
        .annotate(count=Count('student__interest'))
        .order_by('count')[:5]
    )
    distinct_interests_count = Interest.objects.values('name').distinct().count()
    total_students = Student.objects.count()
    today = date.today()

    studying_students_count = Student.objects.filter(start_date__lte=today, end_date__gte=today).count()

    recent_enrollment_date = today - timedelta(days=90)
    recently_enrolled_count = Student.objects.filter(start_date__gte=recent_enrollment_date).count()

    about_to_graduate_date = today + timedelta(days=180)
    about_to_graduate_count = Student.objects.filter(end_date__lte=about_to_graduate_date).count()

    graduated_students_count = Student.objects.filter(end_date__lt=today).count()

    context = {
        'top_interests': top_interests,
        'bottom_interests': bottom_interests,
        'distinct_interests_count': distinct_interests_count,
        'total_students': total_students,
        'studying_students_count': studying_students_count,
        'recently_enrolled_count': recently_enrolled_count,
        'about_to_graduate_count': about_to_graduate_count,
        'graduated_students_count': graduated_students_count,
    }
    return render(request, 'student_dashboard.html', context)