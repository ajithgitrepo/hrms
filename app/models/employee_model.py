# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group
from app.models.department_model import Department 

# Create your models here.

class Employee(models.Model):  
    boolChoice = (
        ("M","Male"),("F","Female")
        )
#     MARITAL_MALE = 'M'
#     MARITAL_FEMALE = 'F'
#     MARITAL_CHOICES = (
#         (MARITAL_MALE, 'Male', ), 
#         (MARITAL_FEMALE, 'Female', ), 
#     )
#    user = models.ForeignKey(Group, related_name='role', on_delete=models.CASCADE)

    employee_id = models.CharField(primary_key=True,max_length=20, blank = False, null = False)  
    first_name = models.CharField(max_length=30 , blank = False, null = False)
    last_name = models.CharField(max_length=30)  
    email_id = models.EmailField(max_length=50)  
    mobile_number = models.CharField(max_length=12) 
    created_at = models.DateTimeField(auto_now_add = True)
    nick_name = models.CharField(max_length=30) 
    emirate_id = models.CharField(max_length=30, blank = True, null = True) 
    department = models.ForeignKey(Department, max_length=50, blank=True, related_name='department_emp', null=True, on_delete= models.SET_NULL)
    # reporting_to = models.CharField(max_length=20, blank = True, null = True)  
    source_of_hire = models.CharField(max_length=200, blank = True, null = True)  
    seating_location = models.CharField(max_length=50, blank = True, null = True)  
    location = models.CharField(max_length=50, blank = True, null = True)  
    title = models.CharField(max_length=80, blank = True, null = True)  
    date_of_joining = models.DateField( blank = True, null = True)  
    employee_status = models.CharField(max_length=20, blank = True, null = True)  
    employee_type = models.CharField(max_length=20, blank = True, null = True)  
    work_phone = models.CharField(max_length=20, blank = True, null = True)  
    code_name = models.CharField(max_length=50, blank = True, null = True)  
    code_num = models.CharField(max_length=50, blank = True, null = True)  
    extension = models.CharField(max_length=20, blank = True, null = True)  
    role = models.ForeignKey(Group, blank=True, related_name='role', null=True, on_delete= models.SET_NULL)
    total_experience = models.CharField(max_length=20, blank = True, null = True)  
    experience = models.CharField(max_length=20, blank = True, null = True)  

    mobile_phone = models.CharField(max_length=20, blank = True, null = True)
    #code_name = models.CharField(max_length=30) 
    #code_num = models.CharField(max_length=30) 
    
    other_email = models.CharField(max_length=20, blank = True, null = True)  
    birth_date = models.DateField( blank = True, null = True)  
    marital_status = models.CharField(max_length=20, choices= boolChoice,  blank = True, null = True)  
    address = models.TextField (blank = True, null = True)  
    tags = models.CharField(max_length=20, blank = True, null = True)  

    job_description = models.CharField(max_length=500, blank = True, null = True)  
    expertise = models.CharField(max_length=200, blank = True, null = True)  
    date_of_exit = models.DateField( blank = True, null = True)  
    gender = models.TextField (max_length=20,blank = True, null = True)  
    about_me = models.CharField(max_length=500, blank = True, null = True)  
    
    
    #added_by = models.CharField(max_length=30) 
    #added_time = models.DateTimeField() 
    #modified_by = models.CharField(max_length=30)
    #modified_time = models.TimeField()
    #created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    profile = models.ImageField(blank = True, null = True)
      
    class Meta:  
        db_table = "employee"  

class Work_Experience(models.Model):
    id = models.IntegerField(primary_key = True) 
#     employee_id = models.CharField(max_length=250, blank = True, null=True) 
    previous_company_name = models.CharField(max_length=180, blank = True, null=True) 
    job_title = models.CharField(max_length=180, blank = True, null=True) 
    from_date = models.DateField(blank = True, null=True) 
    to_date = models.DateField(blank = True, null=True) 
    job_description = models.CharField(max_length=1000, blank = True, null=True)
    is_active = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)

    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)


    class Meta:  
        db_table = "work_experience"


class Education(models.Model):
    id = models.IntegerField(primary_key = True) 
    school_name = models.CharField(max_length=180, blank = True, null=True) 
    degree = models.CharField(max_length=180, blank = True, null=True) 
    field = models.CharField(max_length=180, blank = True, null=True) 
    date_of_completion = models.DateField(blank = True, null=True) 
    notes = models.CharField(max_length=1000, blank = True, null=True)
    interests = models.CharField(max_length=1000, blank = True, null=True)
    is_active = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)

    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)


    class Meta:  
        db_table = "education" 

class Dependent(models.Model):
    id = models.AutoField(primary_key=True)
    dependent_name = models.CharField(max_length=180, blank = True, null=True) 
    relationship = models.CharField(max_length=180, blank = True, null=True) 
    date_of_birth = models.DateField(blank = True, null=True) 
    is_active = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)

    # employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)


    class Meta:  
        db_table = "dependent" 

# Group.add_to_class('role_type', models.CharField(max_length=180,null=True))
# Group.add_to_class('description', models.CharField(max_length=180,null=True))
# Group.add_to_class('created_at', models.DateTimeField(auto_now_add=True, null=True))

# Group.add_to_class('created_by', models.CharField(max_length=180, null=True))

# Group.add_to_class('updated_at', models.DateTimeField(auto_now_add=True, null=True))
# Group.add_to_class('is_active', models.CharField(max_length=50,null=True, blank=True,default='1'))