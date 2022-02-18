# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
# from django.contrib.auth.models import User


# Create your models here.

class Weekend(models.Model):
   
    id = models.AutoField(primary_key=True)
    week_starts_on= models.CharField(max_length=30, blank = False, null = False )
    week_ends_on = models.CharField(max_length=30, blank = False, null = False)
    week_off = models.CharField(max_length=30,blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True)  

      
    class Meta:  
        db_table = "weekend"

 