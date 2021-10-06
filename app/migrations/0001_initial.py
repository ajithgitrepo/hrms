# Generated by Django 3.2.5 on 2021-08-07 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.CharField(max_length=20,primary_key=True,serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email_id', models.EmailField(max_length=50)),
                ('mobile_number', models.CharField(max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('nick_name', models.CharField(max_length=30)),
                ('department', models.CharField(blank=True, max_length=20, null=True)),
                ('reporting_to', models.CharField(blank=True, max_length=20, null=True)),
                ('source_of_hire', models.CharField(blank=True, max_length=200, null=True)),
                ('seating_location', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=80, null=True)),
                ('date_of_joining', models.DateField(blank=True, null=True)),
                ('employee_status', models.CharField(blank=True, max_length=20, null=True)),
                ('employee_type', models.CharField(blank=True, max_length=20, null=True)),
                ('work_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('extension', models.CharField(blank=True, max_length=20, null=True)),
                ('role', models.IntegerField(blank=True, null=True)),
                ('total_experience', models.CharField(blank=True, max_length=20, null=True)),
                ('experience', models.CharField(blank=True, max_length=20, null=True)),
                ('mobile_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('other_email', models.CharField(blank=True, max_length=20, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('tags', models.CharField(blank=True, max_length=20, null=True)),
                ('job_description', models.CharField(blank=True, max_length=500, null=True)),
                ('expertise', models.CharField(blank=True, max_length=200, null=True)),
                ('date_of_exit', models.DateField(blank=True, null=True)),
                ('gender', models.TextField(blank=True, max_length=20, null=True)),
                ('about_me', models.CharField(blank=True, max_length=500, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
             
            ],
            options={
                'db_table': 'employee',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
