# Generated by Django 3.2.5 on 2021-08-13 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210812_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave_type',
            name='color',
            field=models.CharField(blank=True, default=0, max_length=50, null=True),
        ),
    ]
