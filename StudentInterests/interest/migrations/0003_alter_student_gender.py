# Generated by Django 4.1.4 on 2023-12-22 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0002_student_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=7),
        ),
    ]
