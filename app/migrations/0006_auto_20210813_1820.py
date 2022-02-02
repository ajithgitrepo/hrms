# Generated by Django 3.2.5 on 2021-08-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_leave_type_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave_effective',
            name='reset_carry_count',
            field=models.CharField(blank=True, default=0, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='leave_effective',
            name='reset_carry_enc_count',
            field=models.CharField(blank=True, default=0, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='leave_effective',
            name='reset_carry_enc_method',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
