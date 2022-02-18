<<<<<<< HEAD
# Generated by Django 3.2.5 on 2021-10-22 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_calendar_detail_holiday_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporting_to',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.PositiveSmallIntegerField(default=1)),
                ('device', models.CharField(blank=True, max_length=20, null=True)),
                ('employee', models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report_employee', to='app.employee')),
                ('reporting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporting_to_employee', to='app.employee')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporting_updated', to='app.employee')),
            ],
            options={
                'db_table': 'reporting_to',
            },
        ),
    ]
=======
# Generated by Django 3.2.5 on 2021-10-22 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_calendar_detail_holiday_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporting_to',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.PositiveSmallIntegerField(default=1)),
                ('device', models.CharField(blank=True, max_length=20, null=True)),
                ('employee', models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report_employee', to='app.employee')),
                ('reporting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporting_to_employee', to='app.employee')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporting_updated', to='app.employee')),
            ],
            options={
                'db_table': 'reporting_to',
            },
        ),
    ]
>>>>>>> origin/hrms-09-02-2022
