
from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Leave_Type(models.Model): 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255 , blank = False, null = False)
    color = models.CharField(max_length=50,blank = True, null = True, default=000)  
    image = models.CharField(max_length=255,blank = True, null = True)  
    code = models.CharField(max_length=255,blank = True, null = True)  
    type = models.CharField(max_length=255) 
    unit = models.CharField(max_length=255) 
    description = models.CharField(max_length=255,blank = True, null = True)
    validity_from = models.DateField(blank = True, null=True) 
    validity_to = models.DateField(blank = True, null=True) 
   
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)

    class Meta:  
        db_table = "leave_type" 



class Leave_Effective(models.Model): 
    id = models.AutoField(primary_key=True)
    leave_type = models.ForeignKey(Leave_Type, blank=True, null=True, related_name='leave_type_id_effective', on_delete= models.SET_NULL)
    effective_after = models.CharField(max_length=255) 
    effective_period = models.CharField(max_length=255) 
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
        db_table = "leave_effective" 

   
class Leave_Applicable(models.Model):
    id = models.AutoField(primary_key=True)
    leave_type = models.ForeignKey(Leave_Type, blank=True, null=True, related_name='leave_type_id_applicable', on_delete= models.SET_NULL)
    gender = models.CharField(max_length=255,blank = True, null=True) 
    marital_status = models.CharField(max_length=255,blank = True, null=True) 
    department = models.CharField(max_length=255,blank = True, null=True) 
    designation = models.CharField(max_length=255,blank = True, null=True) 
    location = models.CharField(max_length=255,blank = True, null=True) 
    role = models.CharField(max_length=255,blank = True, null=True) 
    employment_type = models.CharField(max_length=255,blank = True, null=True) 
    source_of_hire = models.CharField(max_length=255,blank = True, null=True) 
    onboarding_status = models.CharField(max_length=255,blank = True, null=True) 

    all_employees = models.CharField(max_length=255, default=1, blank = True, null=True) 

    exception_dept = models.CharField(max_length=255,blank = True, null=True) 
    exception_desgn = models.CharField(max_length=255,blank = True, null=True) 
    exception_location = models.CharField(max_length=255,blank = True, null=True) 
    exception_role = models.CharField(max_length=255,blank = True, null=True) 
    exception_emp_type = models.CharField(max_length=255,blank = True, null=True) 

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)

    class Meta:  
        db_table = "leave_applicable" 

class Leave_Restrictions(models.Model):
    id = models.AutoField(primary_key=True)
    leave_type = models.ForeignKey(Leave_Type, blank=True, null=True, related_name='leave_type_id_restrictions', on_delete= models.SET_NULL)
    weekend_bw_leave = models.CharField(max_length=255, default=0, blank = True, null=True)
    weekend_bw_leave_days = models.CharField(max_length=255, default=0, blank = True, null=True) 
    holydays_bw_leave = models.CharField(max_length=255, default=0, blank = True, null=True)
    holydays_bw_leave_days = models.CharField(max_length=255, default=0, blank = True, null=True) 
    exceeds_leave_balance = models.CharField(max_length=255, blank = True, null=True)
    duration = models.CharField(max_length=255, blank = True, null=True)
    allow_users_to_view = models.CharField(max_length=255, blank = True, null=True)
    balance_to_display = models.CharField(max_length=255, default=0, blank = True, null=True) 
    minimum_leave_apply = models.CharField(max_length=255, default=0, blank = True, null=True) 
    maximum_leave_apply = models.CharField(max_length=255, default=0, blank = True, null=True) 
    maximum_consecutive_leave_apply = models.CharField(max_length=255, default=0, blank = True, null=True) 
    minimum_gap_apply = models.CharField(max_length=255, default=0, blank = True, null=True) 
    maximum_application = models.CharField(max_length=255, default=0, blank = True, null=True)
    maximum_application_period = models.CharField(max_length=255, blank = True, null=True)
    leave_only_on = models.CharField(max_length=255, blank = True, null=True)
    leave_cannot_taken_with = models.CharField(max_length=255, blank = True, null=True)
    leave_request_past_days = models.CharField(max_length=255, default=0, blank = True, null=True)
    past_days_check = models.CharField(max_length=255, default=0, blank = True, null=True)
    past_days_count = models.CharField(max_length=255, blank = True, null=True)
    leave_request_future_days = models.CharField(max_length=255, default=0, blank = True, null=True)
    leave_request_next_check = models.CharField(max_length=255, default=0, blank = True, null=True)
    leave_request_next_count = models.CharField(max_length=255, blank = True, null=True)
    leave_request_apply_check = models.CharField(max_length=255, default=0, blank = True, null=True)
    leave_request_apply_count = models.CharField(max_length=255, blank = True, null=True)
    file_upload_after = models.CharField(max_length=255, default=0, blank = True, null=True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    is_active = models.PositiveSmallIntegerField(default=1)

    class Meta:  
        db_table = "leave_resctictions" 