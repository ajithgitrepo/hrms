# Generated by Django 3.2.5 on 2022-01-03 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0067_auto_20211231_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='is_wfh_approved',
        ),
        migrations.AddField(
            model_name='attendance',
            name='is_half',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='leaverequest',
            name='leave_mode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='total_days',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
