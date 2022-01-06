# Generated by Django 3.2.5 on 2022-01-05 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0076_attendance_is_half'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='checkin_active',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='checkout_active',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
