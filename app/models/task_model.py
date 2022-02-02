# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User
from app.models.employee_model import Employee
from django.contrib.auth.models import Group

import random



# Create your models here.

class Task(models.Model):
   
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, blank=False, null=True, on_delete= models.SET_NULL)
    task_name = models.CharField(max_length=300, blank = False, null = False)
    
    description = models.CharField(max_length=500,blank = False, null = False)
    start_date = models.DateField(max_length=30,blank = False, null = False)
    end_date=models.DateField(max_length=30,blank = False, null = False)
    reminder=models.DateField(max_length=30,blank = False, null = False)
    priority=models.CharField(max_length=30,blank = False, null = False)
    status=models.CharField(max_length=30,blank = False, null = False)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True)  

      
    class Meta:  
        db_table = "task"

 