# Generated by Django 4.1.4 on 2023-12-25 10:49

from django.db import migrations, models
import interest.models


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='permissions',
            field=models.ManyToManyField(default=interest.models.Permission.create_default_permission, to='interest.permission'),
        ),
    ]
