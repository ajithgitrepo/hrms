
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from app.models.leave_type_model import Leave_Type 
from app.models.employee_model import Employee 


# class Leave_Type(models.Model): 
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255 , blank = False, null = False)
#     color = models.CharField(max_length=50,blank = True, null = True, default=000)  
#     image = models.CharField(max_length=255,blank = True, null = True)  
#     code = models.CharField(max_length=255,blank = True, null = True)  
#     type = models.CharField(max_length=255) 
#     unit = models.CharField(max_length=255) 
#     description = models.CharField(max_length=255,blank = True, null = True)
#     validity_from = models.DateField(blank = True, null=True) 
#     validity_to = models.DateField(blank = True, null=True) 
#     color = models.CharField(max_length=255, blank = True, null=True) 

   
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now_add = True)
#     is_active = models.PositiveSmallIntegerField(default=1)

#     class Meta:  
#         db_table = "leave_type" 


class Customize_Leave_Effective(models.Model): 
    id = models.AutoField(primary_key=True)
    leave_type = models.ForeignKey(Leave_Type, blank=True, null=True, on_delete= models.SET_NULL)
   # employee_id = models.CharField(max_length=255) 
    employee_id = models.ForeignKey(Employee, blank=True, null=True, on_delete= models.SET_NULL)
    effective_after = models.CharField(max_length=255) 
    effective_period = models.CharField(max_length=255) 
    effective_from = models.CharField(max_length=255) 
   
    effective_from_date = models.DateField(blank = True, null=True) 

    effective_from = models.CharField(max_length=255) 
    accrual = models.CharField(max_length=255,default=0,blank = True, null=True) 
    accrual_period = models.CharField(max_length=255,blank = True, null=True) 
    effective_on = models.CharField(max_length=255,blank = True, null=True) 
    effective_month = models.CharField(max_length=255,blank = True, null=True) 
    effective_no_of_days = models.CharField(max_length=255,default=0,blank = True, null=True) 
    effective_in = models.CharField(max_length=255,blank = True, null=True) 

    reset = models.CharField(max_length=255,default=0,blank = True, null=True) 
    reset_period = models.CharField(max_length=255,blank = True, null=True) 
    reset_on = models.CharField(max_length=255,blank = True, null=True) 
    reset_month = models.CharField(max_length=255,blank = True, null=True) 
    reset_carry_forward = models.CharField(max_length=255,default=0,blank = True, null=True) 
    reset_carry_count = models.CharField(max_length=255,default=0,blank = True, null=True) 
    reset_carry_method = models.CharField(max_length=255,blank = True, null=True) 
    reset_carry_forward_max = models.CharField(max_length=255,blank = True, null=True) 
    reset_carry_forward_overall_limit = models.CharField(max_length=255,blank = True, null=True) 
    reset_carry_encashment = models.CharField(max_length=255,default=0,blank = True, null=True) 
    reset_carry_enc_count = models.CharField(max_length=255,default=0,blank = True, null=True) 
    reset_carry_enc_method = models.CharField(max_length=255,blank = True, null=True) 
    reset_encashment_forward_max = models.CharField(max_length=255,blank = True, null=True) 
    reset_carry_forward_expiry_in = models.CharField(max_length=255, default=0, blank = True, null=True) 
    reset_carry_forward_expiry_month = models.CharField(max_length=255,blank = True, null=True) 

    opening_balance = models.CharField(max_length=255,default=0,blank = True, null=True) 
    maximum_balance = models.CharField(max_length=255,default=0,blank = True, null=True) 

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)

    class Meta:  
        db_table = "customize_leave_effective" 

