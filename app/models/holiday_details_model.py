from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group
from app.models.employee_model import Employee 
from app.models.location_model import Location

import random

# Create your models here.

class Holiday_Detail(models.Model): 

    # Separation

    id = models.AutoField(primary_key=True)  
    holiday_name = models.CharField(max_length=50, blank = True, null = True) 
    type = models.CharField(max_length=50, blank = True, null = True)   
    date = models.DateField(max_length=30 , blank = False, null = False)
    description = models.TextField( blank = True, null = True)  
    applicable_location = models.ForeignKey(Location, blank=True, null=True, related_name='holiday_location', on_delete= models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)
  
    class Meta:  
        db_table = "holiday_details"  

