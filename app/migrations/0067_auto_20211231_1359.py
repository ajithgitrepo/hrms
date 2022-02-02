# Generated by Django 3.2.5 on 2021-12-31 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0066_client_project_timelogs'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel_expense_detail',
            name='is_approved',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='travel_expense_detail',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='travel_expence_updated', to='app.employee'),
        ),
        migrations.AlterField(
            model_name='travel_expense_detail',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='travel_expence_employee', to='app.employee'),
        ),
    ]
