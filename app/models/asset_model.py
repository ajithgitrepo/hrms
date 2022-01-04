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

class Asset_Detail(models.Model): 

    # Separation

    id = models.AutoField(primary_key=True)  
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)
    type_of_asset = models.CharField(max_length=30 , blank = False, null = False)
    given_date = models.DateField(blank = True, null = True)  
    return_date = models.DateField( blank = True, null = True) 
    asset_details = models.TextField( blank = True, null = True)  

    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)

    updated_by = models.ForeignKey(Employee, blank=True, null=True, related_name='asset_approve', on_delete= models.SET_NULL)
    is_approved = models.CharField(max_length=20, blank = True, null = True,default=0)
  
    class Meta:  
        db_table = "asset_details"  

