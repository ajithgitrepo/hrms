
from django.db import models
from django.contrib.auth.models import User 
from app.models.employee_model import *


# Create your models here.

class Reporting(models.Model):  
   
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, max_length=50, blank=True, related_name='report_employee', null=True, on_delete= models.SET_NULL)
    reporting = models.ForeignKey(Employee, blank=True, null=True, related_name='reporting_to_employee', on_delete= models.SET_NULL)
    updated_by = models.ForeignKey(Employee, blank=True, null=True, related_name='reporting_updated', on_delete= models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True)  
   
      
    class Meta:  
        db_table = "reporting_to"  

 