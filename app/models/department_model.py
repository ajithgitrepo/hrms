# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 


# Create your models here.

class Department(models.Model):  
   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank = False, null = False)  
    description = models.CharField(max_length=300, blank = False, null = False)  
    
    added_by = models.CharField(max_length=30,blank = True, null = True) 
    updated_by = models.CharField(max_length=30,blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True)  

      
    class Meta:  
        db_table = "department"  

 