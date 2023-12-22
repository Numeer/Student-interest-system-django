from datetime import date, timedelta, datetime
import json
from django.forms import DurationField, model_to_dict
from django.http import JsonResponse
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, redirect, render
from interest.StudentForm import StudentForm
from django.db.models import Count, F, ExpressionWrapper, IntegerField
from interest.models import ActivityLog, Interest, Student
from django.db.models.functions import ExtractYear
from django.db.models import F, ExpressionWrapper, fields
from django.db.models import Value, DateField
from django.db.models.functions import ExtractYear, ExtractMonth
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

    about_to_graduate_date = today + timedelta(days=90)
    about_to_graduate_count = Student.objects.filter(end_date__lte=about_to_graduate_date, end_date__gt=today).count()

    graduated_students_count = Student.objects.filter(end_date__lt=today).count()

    # Provincial distribution - Fetch province distribution data for pie chart
    province_data = Student.objects.values('city').annotate(count=Count('id'))

    province_labels = [item['city'] for item in province_data]
    province_counts = [item['count'] for item in province_data]

    # Submission chart - Fetch daily student creation data for the last 30 days for line chart
    today = date.today()
    last_30_days = today - timedelta(days=30)
    daily_submissions = (
        Student.objects.filter(start_date__gte=last_30_days)
        .values('start_date')
        .annotate(count=Count('id'))
        .order_by('start_date')
    )

    submission_dates = [item['start_date'].strftime('%Y-%m-%d') for item in daily_submissions]
    submission_counts = [item['count'] for item in daily_submissions]

    # Age distribution - Fetch age data for bar chart
    age_data = (
        Student.objects.annotate(
            years_diff=ExtractYear('date_of_birth') - ExtractYear(datetime.now()),
            months_diff=ExtractMonth('date_of_birth') - ExtractMonth(datetime.now())
        )
        .annotate(
            age=ExpressionWrapper(
                (F('years_diff') * 12 + F('months_diff')) / 12,
                output_field=IntegerField()
            )
        )
        .values('age')
        .annotate(count=Count('id'))
        .order_by('age')
    )

    age_groups = [int(item['age']) for item in age_data]
    age_counts = [item['count'] for item in age_data]

    # Department distribution - Fetch department data for pie chart
    department_data = Student.objects.values('department').annotate(count=Count('id'))

    department_labels = [item['department'] for item in department_data]
    department_counts = [item['count'] for item in department_data]

    # Degree distribution - Fetch degree title data for pie chart
    degree_data = Student.objects.values('degree_title').annotate(count=Count('id'))

    degree_labels = [item['degree_title'] for item in degree_data]
    degree_counts = [item['count'] for item in degree_data]

    # Gender distribution - Fetch gender data for pie chart
    gender_data = Student.objects.values('gender').annotate(count=Count('id'))

    gender_labels = [item['gender'] for item in gender_data]
    gender_counts = [item['count'] for item in gender_data]
    context = {
        'top_interests': top_interests,
        'bottom_interests': bottom_interests,
        'distinct_interests_count': distinct_interests_count,
        'total_students': total_students,
        'studying_students_count': studying_students_count,
        'recently_enrolled_count': recently_enrolled_count,
        'about_to_graduate_count': about_to_graduate_count,
        'graduated_students_count': graduated_students_count,
        'province_labels': json.dumps(province_labels),
        'province_counts': json.dumps(province_counts),
        'submission_dates': json.dumps(submission_dates),
        'submission_counts': json.dumps(submission_counts),
        'age_groups': json.dumps(age_groups),
        'age_counts': json.dumps(age_counts),
        'department_labels': json.dumps(department_labels),
        'department_counts': json.dumps(department_counts),
        'degree_labels': json.dumps(degree_labels),
        'degree_counts': json.dumps(degree_counts),
        'gender_labels': json.dumps(gender_labels),
        'gender_counts': json.dumps(gender_counts),
    }
    return render(request, 'student_dashboard.html', context)