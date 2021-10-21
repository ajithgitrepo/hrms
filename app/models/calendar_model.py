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

class Calendar_Detail(models.Model): 

    # Separation

    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateField(null=True,blank=True)
    end = models.DateField(null=True,blank=True)
    event_type = models.CharField(max_length=10,null=True,blank=True)

  
    class Meta:  
        db_table = "calendar_details"  
 
    def __str__(self):
        return self.event_name

