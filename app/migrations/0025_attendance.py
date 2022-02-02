# Generated by Django 3.2.5 on 2021-09-27 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_onboard_education_onboard_employee_onboard_work_experience'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('is_present', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('is_leave', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('checkin_time', models.TimeField(blank=True, null=True)),
                ('checkout_time', models.TimeField(blank=True, null=True)),
                ('is_leave_approved', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('is_active', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_id_attendance', to='app.employee')),
                ('leave_approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_by_attendance', to='app.employee')),
            ],
            options={
                'db_table': 'attendance',
            },
        ),
    ]
