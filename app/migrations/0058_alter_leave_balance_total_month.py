# Generated by Django 3.2.5 on 2021-12-01 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0057_auto_20211129_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave_balance',
            name='total_month',
            field=models.CharField(default=0, max_length=30),
        ),
    ]
