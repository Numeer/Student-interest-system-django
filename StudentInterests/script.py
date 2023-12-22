from datetime import date
from django.utils import timezone
from interest.models import Student, Interest  # Import your Student and Interest models
from random import choice

# Sample data for demonstration purposes (modify as needed)
GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

DEPARTMENT_CHOICES = (
        ('IT', 'Information Technology'),
        ('CS', 'Computer Science'),
        ('ECE', 'Electronics and Communication'),
        ('Mechanical', 'Mechanical Engineering'),
        ('Civil', 'Civil Engineering'),
        ('Chemical', 'Chemical Engineering'),
        ('Aerospace', 'Aerospace Engineering'),
        ('Electrical', 'Electrical Engineering'),
        ('Biomedical', 'Biomedical Engineering'),
        ('Environmental', 'Environmental Engineering'),
        ('Industrial', 'Industrial Engineering'),
        ('Software', 'Software Engineering'),
        ('Architecture', 'Architecture'),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('Business', 'Business Administration'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Economics', 'Economics'),
        ('Accounting', 'Accounting'),
        ('Management', 'Management'),
        ('Psychology', 'Psychology'),
        ('Sociology', 'Sociology'),
        ('Anthropology', 'Anthropology'),
        ('History', 'History'),
        ('Geography', 'Geography'),
        ('Political Science', 'Political Science'),
        ('Public Administration', 'Public Administration'),
        ('Languages', 'Languages'),
        ('Literature', 'Literature'),
        ('Fine Arts', 'Fine Arts'),
        ('Performing Arts', 'Performing Arts'),
        ('Education', 'Education'),
        ('Nursing', 'Nursing'),
        ('Pharmacy', 'Pharmacy'),
        ('Medicine', 'Medicine'),
        ('Law', 'Law'),
        ('Veterinary Science', 'Veterinary Science'),
        ('Media Studies', 'Media Studies'),
        ('Communication', 'Communication'),
        ('Philosophy', 'Philosophy'),
        ('Religious Studies', 'Religious Studies'),
        ('Computer Applications', 'Computer Applications'),
        ('Data Science', 'Data Science'),
        ('Information Systems', 'Information Systems'),
        ('Library Science', 'Library Science'),
        ('Health Science', 'Health Science'),
        ('Social Work', 'Social Work'),
        ('Supply Chain Management', 'Supply Chain Management'),
        ('Operations Management', 'Operations Management'),
        ('Hospitality Management', 'Hospitality Management'),
        ('Tourism Management', 'Tourism Management'),
        ('Sports Management', 'Sports Management'),
        ('Human Resources', 'Human Resources'),
        ('Other', 'Other'),
    )
    
DEGREE_CHOICES = (
        ('Associate Degree', 'Associate Degree'),
        ('Bachelor Degree', 'Bachelor Degree'),
        ('M.Phil Degree', 'M.Phil Degree'),
        ('Post Graduate Diploma', 'Post Graduate Diploma'),
        ('Doctrate', 'Doctrate'),
        ('Post Doctrate', 'Post Doctrate'),
        ('PhD', 'PhD'),
    )
    
CITY_CHOICES = (
        ('Karachi', 'Karachi'),
        ('Lahore', 'Lahore'),
        ('Islamabad', 'Islamabad'),
        ('Rawalpindi', 'Rawalpindi'),
        ('Faisalabad', 'Faisalabad'),
        ('Multan', 'Multan'),
        ('Gujranwala', 'Gujranwala'),
        ('Quetta', 'Quetta'),
        ('Peshawar', 'Peshawar'),
        ('Hyderabad', 'Hyderabad'),
        ('Sialkot', 'Sialkot'),
        ('Bahawalpur', 'Bahawalpur'),
        ('Sargodha', 'Sargodha'),
        ('Sukkur', 'Sukkur'),
        ('Larkana', 'Larkana'),
        ('Sheikhupura', 'Sheikhupura'),
        ('Jhang', 'Jhang'),
        ('Rahim Yar Khan', 'Rahim Yar Khan'),
        ('Gujrat', 'Gujrat'),
        ('Mardan', 'Mardan'),
        ('Kasur', 'Kasur'),
        ('Dera Ghazi Khan', 'Dera Ghazi Khan'),
        ('Mingora', 'Mingora'),
        ('Nawabshah', 'Nawabshah'),
        ('Okara', 'Okara'),
        ('Mirpur Khas', 'Mirpur Khas'),
        ('Chiniot', 'Chiniot'),
        ('Kamoke', 'Kamoke'),
        ('Sadiqabad', 'Sadiqabad'),
        ('Burewala', 'Burewala'),
        ('Jacobabad', 'Jacobabad'),
        ('Muzaffargarh', 'Muzaffargarh'),
        ('Muridke', 'Muridke'),
        ('Jhelum', 'Jhelum'),
        ('Shikarpur', 'Shikarpur'),
        ('Hafizabad', 'Hafizabad'),
        ('Kohat', 'Kohat'),
        ('Khanewal', 'Khanewal'),
        ('Dadu', 'Dadu'),
        ('Gojra', 'Gojra'),
        ('Mandi Bahauddin', 'Mandi Bahauddin'),
        ('Tando Allahyar', 'Tando Allahyar'),
        ('Daska', 'Daska'),
        ('Pakpattan', 'Pakpattan'),
        ('Bahawalnagar', 'Bahawalnagar'),
        ('Tando Adam', 'Tando Adam'),
        ('Khairpur', 'Khairpur'),
        ('Chishtian', 'Chishtian'),
        ('Charsadda', 'Charsadda'),
        ('Pishin', 'Pishin'),
        ('Hub', 'Hub'),
        ('Kamalia', 'Kamalia'),
        ('Haripur', 'Haripur'),
        ('Nowshera', 'Nowshera'),
        ('Lodhran', 'Lodhran'),
        ('Shahdadkot', 'Shahdadkot'),
        ('Mianwali', 'Mianwali'),
        ('Khanpur', 'Khanpur'),
        ('Hangu', 'Hangu'),
        ('Timargara', 'Timargara'),
        ('Bannu', 'Bannu'),
        ('Jatoi', 'Jatoi'),
        ('Chakwal', 'Chakwal'),
        ('Kohlu', 'Kohlu'),
        ('Khuzdar', 'Khuzdar'),
        ('Badin', 'Badin'),
        ('Layyah', 'Layyah'),
        ('Loralai', 'Loralai'),
        ('Kasur', 'Kasur'),
        ('Turbat', 'Turbat'),
        ('Mehar', 'Mehar'),
        ('Parachinar', 'Parachinar'),
        ('Gwadar', 'Gwadar'),
        ('Kundian', 'Kundian'),
        ('Shahdadpur', 'Shahdadpur'),
        ('Harunabad', 'Harunabad'),
        ('Ratodero', 'Ratodero'),
        ('Dera Allah Yar', 'Dera Allah Yar'),
        ('Umarkot', 'Umarkot'),
        ('Thatta', 'Thatta'),
        ('Kot Adu', 'Kot Adu'),
        ('Gilgit', 'Gilgit'),
        ('Bhakkar', 'Bhakkar'),
        ('Bagh', 'Bagh'),
        ('Jauharabad', 'Jauharabad'),
        ('Chaman', 'Chaman'),
        ('Leiah', 'Leiah'),
        ('Tando Muhammad Khan', 'Tando Muhammad Khan'),
        ('Dalbandin', 'Dalbandin'),
        ('Nankana Sahib', 'Nankana Sahib'),
        ('Kamber Ali Khan', 'Kamber Ali Khan'),
        ('Mian Channu', 'Mian Channu'),
        ('Tump', 'Tump'),
        ('Kharan', 'Kharan'),
        ('Havelian', 'Havelian'),
        ('Mastung', 'Mastung'),
        ('Beloha', 'Beloha'),
        ('Gakuch', 'Gakuch'),
        ('Pishin', 'Pishin'),
        ('Sibi', 'Sibi'),
        ('Ziarat', 'Ziarat'),
        ('Daur', 'Daur'),
        ('Kachhi', 'Kachhi'),
        ('Uthal', 'Uthal'),
        ('Kalat', 'Kalat'),
        ('Musa Khel Bazar', 'Musa Khel Bazar'),
        ('Hala', 'Hala'),
        ('Mithi', 'Mithi'),
        ('Nasirabad', 'Nasirabad'),
        ('Kharan', 'Kharan'),
        ('Kotri', 'Kotri'),
        ('Shahdadpur', 'Shahdadpur'),
        ('Sanghar', 'Sanghar'),
        ('Zhob', 'Zhob'),
        ('Dera Bugti', 'Dera Bugti'),
        ('Jiwani', 'Jiwani'),
        ('Gandava', 'Gandava'),
        ('Duki', 'Duki'),
        ('Turbat', 'Turbat'),
        ('Tando Jam', 'Tando Jam'),
        ('Tando Allahyar', 'Tando Allahyar'),
        ('Kot Malik Barkhurdar', 'Kot Malik Barkhurdar'),
        ('Sohbatpur', 'Sohbatpur'),
        ('Kandiaro', 'Kandiaro'),
        ('Mansehra', 'Mansehra'),
        ('Kalabagh', 'Kalabagh'),
        ('Karak', 'Karak'),
        ('Mianwali', 'Mianwali'),
        ('Murree', 'Murree'),
        ('Sakrand', 'Sakrand'),
        ('Kandhkot', 'Kandhkot'),
        ('Kot Addu', 'Kot Addu'),
        ('Toba Tek Singh', 'Toba Tek Singh'),
        ('Chichawatni', 'Chichawatni'),
        ('Gujar Khan', 'Gujar Khan'),
        ('Shujaabad', 'Shujaabad'),
        ('Hujra Shah Muqim', 'Hujra Shah Muqim'),
        ('Mailsi', 'Mailsi'),
        ('Tando Ghulam Ali', 'Tando Ghulam Ali'),
        ('Shahkot', 'Shahkot'),
        ('Kashmore', 'Kashmore'),
        ('Mangla', 'Mangla'),
        ('Samundri', 'Samundri'),
        ('Tandlianwala', 'Tandlianwala'),
        ('Jaranwala', 'Jaranwala'),
        ('Shorko', 'Shorko'),
        ('Bakri', 'Bakri'),
        ('Talagang', 'Talagang'),
        ('Pind Dadan Khan', 'Pind Dadan Khan'),
        ('Wah Cantonment', 'Wah Cantonment'),
        ('Ahmadpur East', 'Ahmadpur East'),
        ('Kamra', 'Kamra'),
        ('Bhai Pheru', 'Bhai Pheru'),
        ('Kot Sultan', 'Kot Sultan'),
        ('Vihari', 'Vihari'),
        ('Dipalpur', 'Dipalpur'),
        ('Rajanpur', 'Rajanpur'),
        ('Chuhar Kana', 'Chuhar Kana'),
        ('Renala Khurd', 'Renala Khurd'),
        ('Jalalpur Pirwala', 'Jalalpur Pirwala'),
        ('Chak Azam Saffo', 'Chak Azam Saffo'),
        ('Naushahra Virkan', 'Naushahra Virkan'),
        ('Bhawana', 'Bhawana'),
        ('Lala Musa', 'Lala Musa'),
        ('Kundian', 'Kundian'),
        ('Raiwind', 'Raiwind'),
        ('Kahna', 'Kahna'),
        ('Kot Radha Kishan', 'Kot Radha Kishan'),
        ('Chunian', 'Chunian'),
        ('Tandur', 'Tandur'),
        ('Khairpur', 'Khairpur'),
        ('Mehrabpur', 'Mehrabpur'),
        ('Pindi Bhattian', 'Pindi Bhattian'),
        ('Jam Sahib', 'Jam Sahib'),
        ('Mianwali Bangla', 'Mianwali Bangla'),
        ('Bhopalwala', 'Bhopalwala'),
        ('Zahir Pir', 'Zahir Pir'),
        ('Kot Mumin', 'Kot Mumin'),
        ('Athmuqam', 'Athmuqam'),
        ('Kunri', 'Kunri'),
        ('Khairpur Nathan Shah', 'Khairpur Nathan Shah'),
        ('Jand', 'Jand'),
        ('Naukot', 'Naukot'),
        ('Sarai Alamgir', 'Sarai Alamgir'),
        ('Zafarwal', 'Zafarwal'),
        ('Kahror Pakka', 'Kahror Pakka'),
        ('Gambat', 'Gambat'),
        ('Muridke', 'Muridke'),
        ('Ghotki', 'Ghotki'),
        ('Sobhodero', 'Sobhodero'),
        ('Jahanian Shah', 'Jahanian Shah'),
        ('Mananwala', 'Mananwala'),
        ('Bhakkar', 'Bhakkar'),
        ('Khurrianwala', 'Khurrianwala'),
        ('Darya Khan', 'Darya Khan'),
        ('Kallar Kahar', 'Kallar Kahar'),
        ('Ranipur', 'Ranipur'),
        ('Ubauro', 'Ubauro'),
        ('Kalur Kot', 'Kalur Kot'),
        ('Bela', 'Bela'),
        ('Bhit Shah', 'Bhit Shah'),
        ('Malakwal City', 'Malakwal City'),
        ('Baddomalhi', 'Baddomalhi'),
        ('Faruka', 'Faruka'),
        ('Sahianwala', 'Sahianwala'),
        ('Kot Samaba', 'Kot Samaba'),
        ('Mubarikpur', 'Mubarikpur'),
        ('Rojhan', 'Rojhan'),
        ('Tando Adam Khan', 'Tando Adam Khan'),
        ('Chakwal', 'Chakwal'),
        ('Mehar', 'Mehar'),
        ('Kalaswala', 'Kalaswala'),
        ('Raja Jang', 'Raja Jang'),
        ('Bhawalnagar', 'Bhawalnagar'),
        ('Fort Abbas', 'Fort Abbas'),
        ('Malakwal', 'Malakwal'),
        ('Kameer', 'Kameer'),
        ('Qadirpur Raan', 'Qadirpur Raan'),
        ('Chak Azam Sahu', 'Chak Azam Sahu'),
        ('Saddar Gogera', 'Saddar Gogera'),
        ('Tulamba', 'Tulamba'),
        ('Haveli Lakha', 'Haveli Lakha'),
        ('Dunyapur', 'Dunyapur'),
        ('Hujra', 'Hujra'),
        ('Daira Din Panah', 'Daira Din Panah'),
        ('Kahna Nau', 'Kahna Nau'),
        ('Qasba Gujrat', 'Qasba Gujrat'),
        ('Dera Ismail Khan', 'Dera Ismail Khan'),
        ('Pindi Gheb', 'Pindi Gheb'),
        ('Malakwal Bangla', 'Malakwal Bangla'),
        ('Bholar Dheri', 'Bholar Dheri'),
        ('Chachro', 'Chachro'),
        ('Tobatek Singh', 'Tobatek Singh'),
    )
    

# Assuming you have some Interest objects already created, fetch one for assignment
interest = Interest.objects.first()

# Insert 20 records into the Student model
for i in range(20):
    student = Student.objects.create(
        name=f"Student {i+1}",
        password="some_password",  # Replace with actual passwords or hashing method
        roll_number=f"RollNumber{i+1}",
        email=f"student{i+1}@example.com",
        gender=choice([x[0] for x in GENDER_CHOICES]),
        date_of_birth=date(2000, 1, 1),  # Replace with actual dates of birth
        interest=interest,
        city=choice([x[0] for x in CITY_CHOICES]),
        department=choice([x[0] for x in DEPARTMENT_CHOICES]),
        degree_title=choice([x[0] for x in DEGREE_CHOICES]),
        subject=f"Subject {i+1}",
        start_date=timezone.now(),
        end_date=timezone.now()  # Replace with actual end dates
    )
    student.save()