<<<<<<< HEAD
# Generated by Django 3.2.5 on 2021-09-24 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_employee_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_emp', to='app.department'),
        ),
    ]
=======
# Generated by Django 3.2.5 on 2021-09-24 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_employee_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_emp', to='app.department'),
        ),
    ]
>>>>>>> origin/hrms-09-02-2022
