# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group
from app.models.employee_model import Employee 


# Create your models here.

class Vaccination_Detail(models.Model): 

    # Separation

    id = models.AutoField(primary_key=True)  
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)
    vaccinated_status = models.CharField(max_length=30 , blank = False, null = False)
    vaccin_name = models.CharField(max_length=30 , blank = True, null = True)
    partial_vacci_date = models.DateField(blank = True, null = True)  
    date_of_vaccination = models.DateField( blank = True, null = True) 
    commends = models.TextField( blank = True, null = True)
    partial_url = models.FileField(max_length=500, blank = True, null = True) 
    vaccine_url = models.FileField(max_length=500, blank = True, null = True)   

    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)
  
    class Meta:  
        db_table = "vaccination_details"  

