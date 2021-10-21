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

class Holiday_Detail(models.Model): 

    # Separation

    id = models.AutoField(primary_key=True)  
    holiday_name = models.CharField(max_length=50, blank = True, null = True)  
   # employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)
    date = models.DateField(max_length=30 , blank = False, null = False)
    applicable_location = models.CharField(max_length=450, blank = True, null = True)  
    description = models.TextField( blank = True, null = True)  

    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)
  
    class Meta:  
        db_table = "holiday_details"  

