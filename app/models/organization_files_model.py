# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 
from app.models.employee_model import *


# Create your models here.

class Organization_Files(models.Model):  
   
    id = models.AutoField(primary_key=True)
    file = models.FileField(max_length=254, blank = False, null = False)
    name = models.CharField(max_length=100, blank = False, null = False)  
    description = models.CharField(max_length=300, blank = True, null = True) 
    valid_until = models.DateField(blank = True, null = True) 
    added_by = models.ForeignKey(Employee, blank=True, null=True, related_name='organization_files_added', on_delete= models.SET_NULL)
    updated_by = models.ForeignKey(Employee, blank=True, null=True, related_name='organization_files_updated', on_delete= models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True)  
    folder = models.CharField(max_length=1000, blank = True, null = True)  

    class Meta:  
        db_table = "organization_files"  

 