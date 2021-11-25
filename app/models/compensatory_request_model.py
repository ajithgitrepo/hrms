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

class Compoensatory_Request_Detail(models.Model): 

    # Separation

    id = models.AutoField(primary_key=True,verbose_name ='ID')   
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)
    worked_date = models.DateField(blank = True, null = True) 
    compoensatory_date = models.DateField(blank = True, null = True) 
    unit = models.CharField(max_length=130 , blank = True, null = True)
    duration = models.CharField(max_length=30 , blank = True, null = True)
    from_time = models.TimeField(blank = True, null = True)  
    to_time = models.TimeField(blank = True, null = True)  
    expiry_date = models.DateField( blank = True, null = True) 
    reason = models.CharField(max_length=450 , blank = True, null = True) 
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    status = models.PositiveSmallIntegerField(default=0)
  
    class Meta:  
        db_table = "compensatory_request_details"  

