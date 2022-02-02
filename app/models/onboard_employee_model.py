# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group

import random

# Create your models here.

class Onboard_Employee(models.Model): 

    boolChoice = (
        ("M","Male"),("F","Female")
        )

    # def generate_pk():
    #  number = random.randint(1000, 9999)
    #  res = str('CAD') + str(number)
    #  return res

    candidate_id = models.CharField(primary_key=True,max_length=20, blank = False, null = False)  
    first_name = models.CharField(max_length=30 , blank = False, null = False)
    last_name = models.CharField(max_length=30)  
    email_id = models.EmailField(max_length=50)  
    code_name = models.CharField(max_length=50, blank = True, null = True)  
    code_num = models.CharField(max_length=50, blank = True, null = True)  
    mobile_number = models.CharField(max_length=15, blank = False, null = False) 
    official_email_id = models.CharField(max_length=50, blank = True, null = True) 
    emirate_id = models.CharField(max_length=50, blank = False, null = False) 
    photo_url = models.FileField(max_length=500, blank = True, null = True)

    # Address
    address = models.TextField (blank = True, null = True) 
    state = models.CharField(max_length=20, blank = True, null = True) 
    city = models.CharField(max_length=20, blank = True, null = True) 
    pin_code = models.CharField(max_length=20, blank = True, null = True) 
    country = models.CharField(max_length=20, blank = False, null = False) 

    # Professional Details

    experience = models.CharField(max_length=20, blank = True, null = True) 
    source_of_hire = models.CharField(max_length=200, blank = True, null = True) 
    skill_set = models.CharField(max_length=250, blank = True, null = True)  
    highest_qualify = models.CharField(max_length=250, blank = True, null = True)
    additional_info = models.CharField(max_length=550, blank = True, null = True) 
    current_sal = models.CharField(max_length=550, blank = True, null = True) 
    offer_letter_url = models.CharField(max_length=550, blank = True, null = True) 
    tentative_joining_date = models.DateField( blank = True, null = True) 
    location = models.CharField(max_length=50, blank = True, null = True) 
    title = models.CharField(max_length=80, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)
  
    class Meta:  
        db_table = "onboard_employee"  


class Onboard_Work_Experience(models.Model):
    id = models.IntegerField(primary_key = True) 
    candidate = models.ForeignKey(Onboard_Employee, blank=True, null=True, on_delete= models.SET_NULL)
    previous_company_name = models.CharField(max_length=180, blank = True, null=True) 
    job_title = models.CharField(max_length=180, blank = True, null=True) 
    from_date = models.DateField(blank = True, null=True) 
    to_date = models.DateField(blank = True, null=True) 
    job_description = models.CharField(max_length=1000, blank = True, null=True)
    is_active = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)

 

    class Meta:  
        db_table = "onboard_work_experience"

class Onboard_Education(models.Model):
    id = models.IntegerField(primary_key = True) 
    candidate = models.ForeignKey(Onboard_Employee, blank=True, null=True, on_delete= models.SET_NULL)
    school_name = models.CharField(max_length=180, blank = True, null=True) 
    degree = models.CharField(max_length=180, blank = True, null=True) 
    field = models.CharField(max_length=180, blank = True, null=True) 
    date_of_completion = models.DateField(blank = True, null=True) 
    notes = models.CharField(max_length=1000, blank = True, null=True)
    interests = models.CharField(max_length=1000, blank = True, null=True)
    is_active = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)

   

    class Meta:  
        db_table = "onboard_education" 

# class Dependent(models.Model):
#     id = models.AutoField(primary_key=True)
#     dependent_name = models.CharField(max_length=180, blank = True, null=True) 
#     relationship = models.CharField(max_length=180, blank = True, null=True) 
#     date_of_birth = models.DateField(blank = True, null=True) 
#     is_active = models.PositiveSmallIntegerField(default=1)
#     created_at = models.DateTimeField(auto_now_add = True) 
#     updated_at = models.DateTimeField(auto_now_add = True)

#     # employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)


#     class Meta:  
#         db_table = "dependent" 

# Group.add_to_class('role_type', models.CharField(max_length=180,null=True))
# Group.add_to_class('description', models.CharField(max_length=180,null=True))
# Group.add_to_class('created_at', models.DateTimeField(auto_now_add=True, null=True))

# Group.add_to_class('created_by', models.CharField(max_length=180, null=True))

# Group.add_to_class('updated_at', models.DateTimeField(auto_now_add=True, null=True))
# Group.add_to_class('is_active', models.CharField(max_length=50,null=True, blank=True,default='1'))