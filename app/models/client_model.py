# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group

# Create your models here.

class Client(models.Model):  
    
    client_name = models.CharField(max_length=30 , blank = False, null = False)
    first_name = models.CharField(max_length=30 , blank = False, null = False)
    last_name = models.CharField(max_length=30)  
    email_id = models.EmailField(max_length=50)  
    mobile_number = models.CharField(max_length=12) 
    phone = models.CharField(max_length=12) 
    fax = models.CharField(max_length=12) 
    address = models.TextField (blank = False, null = False)  
    city = models.CharField(max_length=30, blank = True, null = True)  
    state = models.CharField(max_length=30, blank = True, null = True)  
    country = models.CharField(max_length=30, blank = True, null = True)  
    pincode = models.CharField(max_length=12) 
    industry = models.CharField(max_length=50, blank = True, null = True)  
    company_size = models.CharField(max_length=20, blank = True, null = True)  
    description = models.TextField (blank = True, null = True)  
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)
      
    class Meta:  
        db_table = "client"  

