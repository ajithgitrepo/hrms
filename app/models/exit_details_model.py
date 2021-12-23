# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group
from app.models.employee_model import Employee 

import random

# Create your models here.

class Exit_Employee_Detail(models.Model): 

    # Separation

    id = models.AutoField(primary_key=True)  
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)
    seperation_date = models.DateField(max_length=30 , blank = False, null = False)
    Interviewer = models.CharField(max_length=30)  
    reason_leaving = models.TextField( blank = True, null = True)  

    # Questionairre

    rejoin_again = models.CharField(max_length=50, blank = True, null = True)  
    like_organi = models.CharField(max_length=50, blank = True, null = True)  
    improve_staff_welfare = models.TextField( blank = True, null = True) 
    share_with_us = models.TextField( blank = True, null = True) 

    # Checklist for Exit Interview
    vehicle_handled = models.CharField(max_length=200, blank = True, null = True) 
    equip_handled = models.CharField(max_length=200, blank = True, null = True)

   
    library_book_submit = models.TextField (blank = True, null = True) 
    security = models.CharField(max_length=200, blank = True, null = True) 
    exit_interv_conduct = models.CharField(max_length=200, blank = True, null = True) 
    notice_period_follow = models.CharField(max_length=200, blank = True, null = True) 
    resignation_letter = models.CharField(max_length=200, blank = True, null = True)
    manager_clearance = models.CharField(max_length=200, blank = True, null = True) 

    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)
  
    class Meta:  
        db_table = "exit_employee_details"  

