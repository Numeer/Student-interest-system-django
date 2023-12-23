from datetime import date, timedelta, datetime
import json
from django.forms import model_to_dict
from django.http import JsonResponse
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, redirect, render
from interest import models
from interest.StudentForm import StudentForm
from django.db.models import Count, F, ExpressionWrapper, IntegerField
from interest.models import ActivityLog, Interest, Student
from django.db.models.functions import ExtractYear
from django.db.models import F, ExpressionWrapper
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractHour
from django.contrib import messages
from django.utils import timezone
from django.db.models.functions import Trunc


def student_login(request):
    if request.method == 'POST':
        rollNo = request.POST.get('username')
        password = request.POST.get('pwd')
        student = Student.objects.filter(roll_number=rollNo, password=password).first()
        if student:
            request.session['logged_in_student_id'] = student.id
            activity = f"Logged in"
            ActivityLog.objects.create(user=student, timestamp=timezone.now(), activity=activity)
            return redirect('student-list')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('login')
    return render(request, 'login.html')


def logout_view(request):
    student_id = request.session.get('logged_in_student_id')
    if student_id:
        student = Student.objects.get(pk=student_id)
        activity = f"Logged out"
        ActivityLog.objects.create(user=student, timestamp=timezone.now(), activity=activity)
        del request.session['logged_in_student_id']
    return redirect('login')


def student_list(request):
    students = Student.objects.all()
    student_id = request.session.get('logged_in_student_id')
    if student_id:
        student = Student.objects.get(pk=student_id)
        activity = f"Viewed student list"
        ActivityLog.objects.create(user=student, timestamp=timezone.now(), activity=activity)
    return render(request, 'student_list.html', {'students': students})


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            student_id = request.session.get('logged_in_student_id')
            student = Student.objects.get(pk=student_id)
            activity = f"Created student"
            ActivityLog.objects.create(user=student, timestamp=timezone.now(), activity=activity)
            return redirect('student-detail', pk=form.instance.pk)
    else:
        form = StudentForm()
        activity = f"Viewed student create form"
        student_id = request.session.get('logged_in_student_id')
        student = Student.objects.get(pk=student_id)
        ActivityLog.objects.create(user=student, timestamp=timezone.now(), activity=activity)
    return render(request, 'student_form.html', {'form': form})


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student_id = request.session.get('logged_in_student_id')
    if student_id:
        student = Student.objects.get(pk=student_id)
        activity = f"Viewed student {student} details"
        ActivityLog.objects.create(user=student, timestamp=timezone.now(), activity=activity)
    return render(request, 'student_detail.html', {'student': student})


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student_id = request.session.get('logged_in_student_id')
            student = Student.objects.get(pk=student_id)
            activity = f"Updated student"
            ActivityLog.objects.create(user=student, timestamp=timezone.now(), activity=activity)
            form.save()
            return redirect('student-list')
    else:
        activity = f"Viewed student update form"
        student_id = request.session.get('logged_in_student_id')
        students = Student.objects.get(pk=student_id)        
        ActivityLog.objects.create(user=students, timestamp=timezone.now(), activity=activity)
        form = StudentForm(instance=student)
    return render(request, 'student_update.html', {'form': form})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        student_id = request.session.get('logged_in_student_id')
        students = Student.objects.get(pk=student_id)
        activity = f"Deleted student"
        ActivityLog.objects.create(user=students, timestamp=timezone.now(), activity=activity)
        return redirect('student-list')
    return render(request, 'student_confirm_delete.html', {'student': student})


def log_activity(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')
        student_id = request.session.get('logged_in_student_id')
        if student_id:
            student = get_object_or_404(Student, pk=student_id)
            ActivityLog.objects.create(user=student, activity=action)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No logged-in student found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def activity_log(request, pk):
    student = get_object_or_404(Student, pk=pk)
    activity_logs = ActivityLog.objects.filter(user=student).values()
    return JsonResponse(list(activity_logs), safe=False)


def student_dashboard(request):
    student_id = request.session.get('logged_in_student_id')
    if student_id:
        student = Student.objects.get(pk=student_id)
        activity = f"Viewed student dashboard"
        ActivityLog.objects.create(user=student, timestamp=timezone.now(), activity=activity)
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

        province_data = Student.objects.values('city').annotate(count=Count('id'))
        province_counts = {}
        for item in province_data:
            city = item['city']
            province = city_province_mapping.get(city, 'Unknown')
            province_counts[province] = province_counts.get(province, 0) + item['count']
        province_labels = list(province_counts.keys())
        province_counts = list(province_counts.values())

        today = date.today()
        thirty_days_ago = timezone.now() - timedelta(days=30)

        student_creation_data = Student.objects.filter(created_at__gte=thirty_days_ago) \
            .extra({'created_day': "date(created_at)"}) \
            .values('created_day') \
            .annotate(total_students=Count('id')) \
            .order_by('created_day')

        chart_data = []
        for data in student_creation_data:
            if data['created_day']:
                date_str = datetime.strptime(data['created_day'], '%Y-%m-%d').strftime('%Y-%m-%d')
                chart_data.append({'date': date_str, 'student_count': data['total_students']})

        chart_data_json = json.dumps(chart_data)

        current_date = timezone.now()
        age_data = (
            Student.objects.annotate(
                years_diff=ExtractYear(current_date) - ExtractYear('date_of_birth'),
                months_diff=ExtractMonth(current_date) - ExtractMonth('date_of_birth')
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

        department_data = Student.objects.values('department').annotate(count=Count('id'))
        department_labels = [item['department'] for item in department_data]
        department_counts = [item['count'] for item in department_data]

        degree_data = Student.objects.values('degree_title').annotate(count=Count('id'))
        degree_labels = [item['degree_title'] for item in degree_data]
        degree_counts = [item['count'] for item in degree_data]

        gender_data = Student.objects.values('gender').annotate(count=Count('id'))
        gender_labels = [item['gender'] for item in gender_data]
        gender_counts = [item['count'] for item in gender_data]
        
        thirty_days_ago = timezone.now() - timedelta(days=30)
        activity_logs_30_days = ActivityLog.objects.filter(timestamp__gte=thirty_days_ago)
        daily_activity_30_days = activity_logs_30_days.extra({'day': "date(timestamp)"}).values('day').annotate(count=Count('id'))
        
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        activity_logs_24_hours = ActivityLog.objects.filter(timestamp__gte=twenty_four_hours_ago)
        activity_counts_24_hours = activity_logs_24_hours.annotate(quarter_hour=Trunc('timestamp', 'minute')).values('quarter_hour').annotate(count=Count('id'))
        
        thirty_days_ago_str = thirty_days_ago.strftime('%Y-%m-%d %H:%M:%S')
        twenty_four_hours_ago_str = twenty_four_hours_ago.strftime('%Y-%m-%d %H:%M:%S')

        daily_activity_30_days_list = list(daily_activity_30_days)
        activity_counts_24_hours_list = list(activity_counts_24_hours)

        daily_activity_30_days_json = json.dumps(daily_activity_30_days_list,default=str)
        activity_counts_24_hours_json = json.dumps(activity_counts_24_hours_list,default=str)
        
        activity_logs_last_30_days = ActivityLog.objects.filter(timestamp__gte=thirty_days_ago)
        activity_counts_per_hour = activity_logs_last_30_days.annotate(hour=ExtractHour('timestamp')).values('hour').annotate(count=Count('id')).order_by('-count')
        
        most_active_hours = [entry['hour'] for entry in activity_counts_per_hour[:3]]
        least_active_hours = [entry['hour'] for entry in activity_counts_per_hour[3:]]
        dead_hours = [entry['hour'] for entry in activity_counts_per_hour if entry['count'] <= 1]
        
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
            'chart_data': chart_data_json,
            'age_groups': json.dumps(age_groups),
            'age_counts': json.dumps(age_counts),
            'department_labels': json.dumps(department_labels),
            'department_counts': json.dumps(department_counts),
            'degree_labels': json.dumps(degree_labels),
            'degree_counts': json.dumps(degree_counts),
            'gender_labels': json.dumps(gender_labels),
            'gender_counts': json.dumps(gender_counts),
            'thirty_days_ago': thirty_days_ago_str,
            'twenty_four_hours_ago': twenty_four_hours_ago_str,
            'daily_activity_30_days': daily_activity_30_days_json,
            'activity_counts_24_hours': activity_counts_24_hours_json,
            'most_active_hours': most_active_hours,
            'least_active_hours': least_active_hours,
            'dead_hours': dead_hours,
        }
    return render(request, 'student_dashboard.html', context)

city_province_mapping = {
    'Karachi': 'Sindh',
    'Lahore': 'Punjab',
    'Islamabad': 'Punjab',
    'Rawalpindi': 'Punjab',
    'Faisalabad': 'Punjab',
    'Multan': 'Punjab',
    'Gujranwala': 'Punjab',
    'Quetta': 'Balochistan',
    'Peshawar': 'Khyber Pakhtunkhwa',
    'Hyderabad': 'Sindh',
    'Sialkot': 'Punjab',
    'Bahawalpur': 'Punjab',
    'Sargodha': 'Punjab',
    'Sukkur': 'Sindh',
    'Larkana': 'Sindh',
    'Sheikhupura': 'Punjab',
    'Jhang': 'Punjab',
    'Rahim Yar Khan': 'Punjab',
    'Gujrat': 'Punjab',
    'Mardan': 'Khyber Pakhtunkhwa',
    'Kasur': 'Punjab',
    'Dera Ghazi Khan': 'Punjab',
    'Mingora': 'Khyber Pakhtunkhwa',
    'Nawabshah': 'Sindh',
    'Okara': 'Punjab',
    'Mirpur Khas': 'Sindh',
    'Chiniot': 'Punjab',
    'Kamoke': 'Punjab',
    'Sadiqabad': 'Punjab',
    'Burewala': 'Punjab',
    'Jacobabad': 'Sindh',
    'Muzaffargarh': 'Punjab',
    'Muridke': 'Punjab',
    'Jhelum': 'Punjab',
    'Shikarpur': 'Sindh',
    'Hafizabad': 'Punjab',
    'Kohat': 'Khyber Pakhtunkhwa',
    'Khanewal': 'Punjab',
    'Dadu': 'Sindh',
    'Gojra': 'Punjab',
    'Mandi Bahauddin': 'Punjab',
    'Tando Allahyar': 'Sindh',
    'Daska': 'Punjab',
    'Pakpattan': 'Punjab',
    'Bahawalnagar': 'Punjab',
    'Tando Adam': 'Sindh',
    'Khairpur': 'Sindh',
    'Chishtian': 'Punjab',
    'Charsadda': 'Khyber Pakhtunkhwa',
    'Pishin': 'Balochistan',
    'Hub': 'Balochistan',
    'Kamalia': 'Punjab',
    'Haripur': 'Khyber Pakhtunkhwa',
    'Nowshera': 'Khyber Pakhtunkhwa',
    'Lodhran': 'Punjab',
    'Shahdadkot': 'Sindh',
    'Mianwali': 'Punjab',
    'Khanpur': 'Punjab',
    'Hangu': 'Khyber Pakhtunkhwa',
    'Timargara': 'Khyber Pakhtunkhwa',
    'Bannu': 'Khyber Pakhtunkhwa',
    'Jatoi': 'Punjab',
    'Chakwal': 'Punjab',
    'Kohlu': 'Balochistan',
    'Khuzdar': 'Balochistan',
    'Badin': 'Sindh',
    'Layyah': 'Punjab',
    'Loralai': 'Balochistan',
    'Turbat': 'Balochistan',
    'Mehar': 'Sindh',
    'Parachinar': 'Khyber Pakhtunkhwa',
    'Gwadar': 'Balochistan',
    'Kundian': 'Punjab',
    'Shahdadpur': 'Sindh',
    'Harunabad': 'Punjab',
    'Ratodero': 'Sindh',
    'Dera Allah Yar': 'Balochistan',
    'Umarkot': 'Sindh',
    'Thatta': 'Sindh',
    'Kot Adu': 'Punjab',
    'Gilgit': 'Gilgit-Baltistan',
    'Bhakkar': 'Punjab',
    'Bagh': 'Azad Kashmir',
    'Jauharabad': 'Punjab',
    'Chaman': 'Balochistan',
    'Leiah': 'Punjab',
    'Tando Muhammad Khan': 'Sindh',
    'Dalbandin': 'Balochistan',
    'Nankana Sahib': 'Punjab',
    'Kamber Ali Khan': 'Sindh',
    'Mian Channu': 'Punjab',
    'Tump': 'Balochistan',
    'Kharan': 'Balochistan',
    'Havelian': 'Khyber Pakhtunkhwa',
    'Mastung': 'Balochistan',
    'Beloha': 'Balochistan',
    'Gakuch': 'Gilgit-Baltistan',
    'Pishin': 'Balochistan',
    'Sibi': 'Balochistan',
    'Ziarat': 'Balochistan',
    'Daur': 'Sindh',
    'Kachhi': 'Balochistan',
    'Uthal': 'Balochistan',
    'Kalat': 'Balochistan',
    'Musa Khel Bazar': 'Khyber Pakhtunkhwa',
    'Hala': 'Sindh',
    'Mithi': 'Sindh',
    'Nasirabad': 'Balochistan',
    'Kharan': 'Balochistan',
    'Kotri': 'Sindh',
    'Shahdadpur': 'Sindh',
    'Sanghar': 'Sindh',
    'Zhob': 'Balochistan',
    'Dera Bugti': 'Balochistan',
    'Jiwani': 'Balochistan',
    'Gandava': 'Balochistan',
    'Duki': 'Balochistan',
    'Turbat': 'Balochistan',
    'Tando Jam': 'Sindh',
    'Tando Allahyar': 'Sindh',
    'Kot Malik Barkhurdar': 'Punjab',
    'Sohbatpur': 'Punjab',
    'Kandiaro': 'Sindh',
    'Mansehra': 'Khyber Pakhtunkhwa',
    'Kalabagh': 'Punjab',
    'Karak': 'Khyber Pakhtunkhwa',
    'Mianwali': 'Punjab',
    'Murree': 'Punjab',
    'Sakrand': 'Sindh',
    'Kandhkot': 'Sindh',
    'Kot Addu': 'Punjab',
    'Toba Tek Singh': 'Punjab',
    'Chichawatni': 'Punjab',
    'Gujar Khan': 'Punjab',
    'Shujaabad': 'Punjab',
    'Hujra Shah Muqim': 'Punjab',
    'Mailsi': 'Punjab',
    'Tando Ghulam Ali': 'Sindh',
    'Shahkot': 'Punjab',
    'Kashmore': 'Sindh',
    'Mangla': 'Punjab',
    'Samundri': 'Punjab',
    'Tandlianwala': 'Punjab',
    'Jaranwala': 'Punjab',
    'Shorko': 'Khyber Pakhtunkhwa',
    'Bakri': 'Punjab',
    'Talagang': 'Punjab',
    'Pind Dadan Khan': 'Punjab',
    'Wah Cantonment': 'Punjab',
    'Ahmadpur East': 'Punjab',
    'Kamra': 'Punjab',
    'Bhai Pheru': 'Punjab',
    'Kot Sultan': 'Punjab',
    'Vihari': 'Punjab',
    'Dipalpur': 'Punjab',
    'Rajanpur': 'Punjab',
    'Chuhar Kana': 'Punjab',
    'Renala Khurd': 'Punjab',
    'Jalalpur Pirwala': 'Punjab',
    'Chak Azam Saffo': 'Punjab',
    'Naushahra Virkan': 'Punjab',
    'Bhawana': 'Punjab',
    'Lala Musa': 'Punjab',
    'Kundian': 'Punjab',
    'Raiwind': 'Punjab',
    'Kahna': 'Punjab',
    'Kot Radha Kishan': 'Punjab',
    'Chunian': 'Punjab',
    'Tandur': 'Sindh',
    'Khairpur': 'Sindh',
    'Mehrabpur': 'Sindh',
    'Pindi Bhattian': 'Punjab',
    'Jam Sahib': 'Sindh',
    'Mianwali Bangla': 'Punjab',
    'Bhopalwala': 'Punjab',
    'Zahir Pir': 'Punjab',
    'Kot Mumin': 'Punjab',
    'Athmuqam': 'Azad Kashmir',
    'Kunri': 'Sindh',
    'Khairpur Nathan Shah': 'Sindh',
    'Jand': 'Punjab',
    'Naukot': 'Sindh',
    'Sarai Alamgir': 'Punjab',
    'Zafarwal': 'Punjab',
    'Kahror Pakka': 'Punjab',
    'Gambat': 'Sindh',
    'Muridke': 'Punjab',
    'Ghotki': 'Sindh',
    'Sobhodero': 'Sindh',
    'Jahanian Shah': 'Punjab',
    'Mananwala': 'Punjab',
    'Bhakkar': 'Punjab',
    'Khurrianwala': 'Punjab',
    'Darya Khan': 'Punjab',
    'Kallar Kahar': 'Punjab',
    'Ranipur': 'Sindh',
    'Ubauro': 'Sindh',
    'Kalur Kot': 'Punjab',
    'Bela': 'Balochistan',
    'Bhit Shah': 'Sindh',
    'Malakwal City': 'Punjab',
    'Baddomalhi': 'Punjab',
    'Faruka': 'Punjab',
    'Sahianwala': 'Punjab',
    'Kot Samaba': 'Punjab',
    'Mubarikpur': 'Punjab',
    'Rojhan': 'Punjab',
    'Tando Adam Khan': 'Sindh',
    'Chakwal': 'Punjab',
    'Mehar': 'Sindh',
    'Kalaswala': 'Punjab',
    'Raja Jang': 'Punjab',
    'Bhawalnagar': 'Punjab',
    'Fort Abbas': 'Punjab',
    'Malakwal': 'Punjab',
    'Kameer': 'Punjab',
    'Qadirpur Raan': 'Punjab',
    'Chak Azam Sahu': 'Punjab',
    'Saddar Gogera': 'Punjab',
    'Tulamba': 'Punjab',
    'Haveli Lakha': 'Punjab',
    'Dunyapur': 'Punjab',
    'Hujra': 'Punjab',
    'Daira Din Panah': 'Punjab',
    'Kahna Nau': 'Punjab',
    'Qasba Gujrat': 'Punjab',
    'Dera Ismail Khan': 'Khyber Pakhtunkhwa',
    'Pindi Gheb': 'Punjab',
    'Malakwal Bangla': 'Punjab',
    'Bholar Dheri': 'Punjab',
    'Chachro': 'Sindh',
    'Tobatek Singh': 'Punjab',
}