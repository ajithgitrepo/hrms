<<<<<<< HEAD
# Generated by Django 3.2.5 on 2021-09-06 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_leave_balance_customize_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customize_Leave_Balance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('balance', models.CharField(blank=True, max_length=30, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.PositiveSmallIntegerField(default=1)),
                ('customize_reason', models.CharField(blank=True, max_length=500, null=True)),
                ('device', models.CharField(blank=True, max_length=20, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_customize', to='app.employee')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_id_customize', to='app.employee')),
                ('leave_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_type_id_customize', to='app.leave_type')),
            ],
            options={
                'db_table': 'customize_leave_balance',
            },
        ),
    ]
=======
# Generated by Django 3.2.5 on 2021-09-06 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_leave_balance_customize_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customize_Leave_Balance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('balance', models.CharField(blank=True, max_length=30, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.PositiveSmallIntegerField(default=1)),
                ('customize_reason', models.CharField(blank=True, max_length=500, null=True)),
                ('device', models.CharField(blank=True, max_length=20, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_customize', to='app.employee')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_id_customize', to='app.employee')),
                ('leave_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_type_id_customize', to='app.leave_type')),
            ],
            options={
                'db_table': 'customize_leave_balance',
            },
        ),
    ]
>>>>>>> origin/hrms-09-02-2022
