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

class Travel_Request_Detail(models.Model): 

    # Separation

    def generate_pk():
      number = random.randint(1000, 9999)
      res = str('TravelID') + str(number)
      return res

    id = models.AutoField(primary_key=True)   
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)
    travel_id = models.CharField(default=generate_pk,max_length=20, db_column='travel_id', unique=True, blank = False, null = False)  
    place_of_visit = models.CharField(max_length=130 , blank = True, null = True)
    employee_department = models.CharField(max_length=30 , blank = True, null = True)
    expected_date_of_arrival = models.DateField(blank = True, null = True)  
    expected_date_of_depature = models.DateField( blank = True, null = True) 
    expected_duration_days = models.CharField(max_length=30 , blank = True, null = True) 
    purpose_of_visit = models.CharField(max_length=30 , blank = True, null = True) 
    customer_name = models.CharField(max_length=30 , blank = True, null = True) 
    billable_to_customer = models.CharField(max_length=20 , blank = True, null = True) 

    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)
  
    class Meta:  
        db_table = "travel_request_details"  

