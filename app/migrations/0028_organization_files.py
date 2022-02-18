<<<<<<< HEAD
# Generated by Django 3.2.5 on 2021-09-29 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20210928_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization_Files',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.CharField(max_length=255)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.PositiveSmallIntegerField(default=1)),
                ('device', models.CharField(blank=True, max_length=20, null=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization_files_added', to='app.employee')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization_files_updated', to='app.employee')),
            ],
            options={
                'db_table': 'organization_files',
            },
        ),
    ]
=======
# Generated by Django 3.2.5 on 2021-09-29 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20210928_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization_Files',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.CharField(max_length=255)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.PositiveSmallIntegerField(default=1)),
                ('device', models.CharField(blank=True, max_length=20, null=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization_files_added', to='app.employee')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization_files_updated', to='app.employee')),
            ],
            options={
                'db_table': 'organization_files',
            },
        ),
    ]
>>>>>>> origin/hrms-09-02-2022
