from django.forms import model_to_dict
from django.http import JsonResponse
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, redirect, render
from interest.StudentForm import StudentForm

from interest.models import ActivityLog, Student

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
    return render(request, 'student_form.html', {'form': form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student-list')
    return render(request, 'student_confirm_delete.html', {'student': student})

# View for displaying activity logs of a specific student
def activity_log(request, pk):
    student = get_object_or_404(Student, pk=pk)
    activity_logs = ActivityLog.objects.filter(user=student).values()  # Get activity logs as dictionaries
    return JsonResponse(list(activity_logs), safe=False)
