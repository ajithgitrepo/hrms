
from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group
from app.models.employee_model import Employee 
from app.models.travel_request_model import Travel_Request_Detail 

import random

# Create your models here.

class Travel_Expense_Detail(models.Model): 

    # Separation

    id = models.AutoField(primary_key=True)   
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL, related_name="travel_expence_employee")
    travel = models.ForeignKey(Travel_Request_Detail,  to_field="travel_id", db_column="travel_id", blank=True, null=True, on_delete= models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    is_approved = models.PositiveSmallIntegerField(default=0)
    updated_by = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL, related_name="travel_expence_updated")

    class Meta:  
        db_table = "travel_expense_details"  

class Travel_Expense_More_Detail(models.Model):
    id = models.AutoField(primary_key = True) 
#     employee_id = models.CharField(max_length=250, blank = True, null=True) 
    description = models.CharField(max_length=180, blank = True, null=True) 
    date = models.DateField(blank = True, null=True) 
    ticket = models.CharField(max_length=180, blank = True, null=True) 
    lodging = models.CharField(max_length=100, blank = True, null=True)
    boarding = models.CharField(max_length=100, blank = True, null=True)
    phone = models.CharField(max_length=100, blank = True, null=True)
    local_conveyance = models.CharField(max_length=100, blank = True, null=True)
    incidentals = models.CharField(max_length=100, blank = True, null=True)
    others = models.CharField(max_length=100, blank = True, null=True)
    currency = models.CharField(max_length=100, blank = True, null=True)
    is_active = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now_add = True)
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)
    travel_exp = models.ForeignKey(Travel_Expense_Detail, blank=True, null=True, on_delete= models.SET_NULL)

    class Meta:  
        db_table = "travel_expense_more_details"