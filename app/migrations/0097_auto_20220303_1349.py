# Generated by Django 3.2.5 on 2022-03-03 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0096_auto_20220303_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='onboard_employee',
            name='visa_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='onboard_employee',
            name='emirate_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
