# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 
from app.models.employee_model import *
from app.models.department_model import *


# Create your models here.

class Announcement(models.Model):  
   
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank = False, null = False) 
    subject = models.CharField(max_length=1000, blank = False, null = False)   
    description = models.CharField(max_length=1000, blank = True, null = True) 
    attachment = models.FileField(max_length=255, blank = True, null = True)  
    department = models.ForeignKey(Department, blank=True, null=True, related_name='announcement_dept', on_delete= models.SET_NULL)
    added_by = models.ForeignKey(Employee, blank=True, null=True, related_name='announcement_added', on_delete= models.SET_NULL)
    updated_by = models.ForeignKey(Employee, blank=True, null=True, related_name='announcement_updated', on_delete= models.SET_NULL)
    expiry_date = models.DateField(blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True)  

      
    class Meta:  
        db_table = "announcements"  

    def __str__(self):
        return self.title

 