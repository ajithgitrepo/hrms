
from django.db import models
from django.contrib.auth.models import User 
from app.models.leave_type_model import *
from app.models.employee_model import *


# Create your models here.

class Leave_Balance(models.Model):  
   
    id = models.AutoField(primary_key=True)
    leave_type = models.ForeignKey(Leave_Type, blank=True, null=True, related_name='leave_type_id_balance', on_delete= models.SET_NULL)
    employee = models.ForeignKey(Employee, blank=True, null=True, related_name='employee_id_balance', on_delete= models.SET_NULL)
    balance = models.CharField(max_length=30,blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True,blank=True, null=True,)
    updated_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    modified_by = models.ForeignKey(Employee, blank=True, null=True, related_name='modified_balance', on_delete= models.SET_NULL)
    modified_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    customize_reason = models.CharField(max_length=500, blank = True, null = True)
    device = models.CharField(max_length=20, blank = True, null = True)  
    total_month = models.CharField(max_length=30,default=0)

    # casual_leave = models.CharField(max_length=30,blank = True, null = True)
    # sick_leave = models.CharField(max_length=30,blank = True, null = True)
    # maternity_eave = models.CharField(max_length=30,blank = True, null = True)
    # Other = models.CharField(max_length=30,blank = True, null = True)
    # paternity_leave= models.CharField(max_length=30,blank = True, null = True)


    class Meta:  
        db_table = "leave_balance"  

 