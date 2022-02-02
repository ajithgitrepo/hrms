# Generated by Django 3.2.5 on 2021-08-12 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [

      
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('added_by', models.CharField(blank=True, max_length=30, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.PositiveSmallIntegerField(default=1)),
                ('device', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dependent_name', models.CharField(blank=True, max_length=180, null=True)),
                ('relationship', models.CharField(blank=True, max_length=180, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('is_active', models.PositiveSmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'dependent',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('school_name', models.CharField(blank=True, max_length=180, null=True)),
                ('degree', models.CharField(blank=True, max_length=180, null=True)),
                ('field', models.CharField(blank=True, max_length=180, null=True)),
                ('date_of_completion', models.DateField(blank=True, null=True)),
                ('notes', models.CharField(blank=True, max_length=1000, null=True)),
                ('interests', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_active', models.PositiveSmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'education',
            },
        ),
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_id', models.CharField(max_length=20)),
                ('leave_type', models.CharField(max_length=30)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('total_days', models.CharField(max_length=12)),
                ('reason', models.TextField(blank=True, null=True)),
                ('is_approved', models.PositiveSmallIntegerField(default=0)),
                ('is_rejected', models.PositiveSmallIntegerField(default=0)),
                ('team_mailid', models.CharField(blank=True, max_length=250, null=True)),
                ('action_by', models.CharField(blank=True, max_length=30, null=True)),
                ('added_by', models.CharField(blank=True, max_length=30, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.PositiveSmallIntegerField(default=1)),
                ('device', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'leave_request',
            },
        ),
        migrations.CreateModel(
            name='Work_Experience',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('previous_company_name', models.CharField(blank=True, max_length=180, null=True)),
                ('job_title', models.CharField(blank=True, max_length=180, null=True)),
                ('from_date', models.DateField(blank=True, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
                ('job_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_active', models.PositiveSmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'work_experience',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='is_active',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
