# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 
from app.models.employee_model import *


# Create your models here.

class Folder(models.Model):  
   
    id = models.AutoField(primary_key=True)
    name = models.FileField(max_length=254, blank = False, null = False)
    added_by = models.ForeignKey(Employee, blank=True, null=True, related_name='folder_added', on_delete= models.SET_NULL)
    updated_by = models.ForeignKey(Employee, blank=True, null=True, related_name='folder_updated', on_delete= models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True)  
   
      
    class Meta:  
        db_table = "folders"  

 