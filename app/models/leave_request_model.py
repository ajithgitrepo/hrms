# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group
from app.models.employee_model import Employee
from app.models.leave_type_model import *

# Create your models here.

class LeaveRequest(models.Model):  
   
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, blank=False, null=True, related_name='employee_id_leave_request', on_delete= models.SET_NULL)
    leave_type = models.ForeignKey(Leave_Type, blank=False, null=True, related_name='leave_type_id_request', on_delete= models.SET_NULL)
    from_date = models.DateField(blank = False, null = False)  
    to_date = models.DateField(blank = False, null = False)  
    total_days = models.FloatField(blank = True, null = True, default=0.0)
    reason = models.TextField (blank = False, null = True)  
    is_approved = models.PositiveSmallIntegerField(default=0)
    is_rejected = models.PositiveSmallIntegerField(default=0) 
    from_time = models.TimeField(blank = True, null = True)  
    to_time = models.TimeField(blank = True, null = True)  

    team_mailid = models.CharField(max_length=250 , blank = False, null = True)

    action_by = models.ForeignKey(Employee, blank=True, null=True, related_name='action_by_leave_request', on_delete= models.SET_NULL)  
    
    added_by = models.ForeignKey(Employee, blank=True, null=True, related_name='added_by_leave_request', on_delete= models.SET_NULL)
    updated_by = models.ForeignKey(Employee, blank=True, null=True, related_name='updated_by_leave_request', on_delete= models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True) 
    document_url = models.FileField(max_length=500, blank = True, null = True)  
    leave_mode = models.CharField(max_length=20, blank = True, null = True)
    leave_part = models.CharField(max_length=20, blank = True, null = True)  

      
    class Meta:  
        db_table = "leave_request"  

   # self.fields[ 'dob' ].input_formats = [ '%Y-%m-%d' ]

# Group.add_to_class('role_type', models.CharField(max_length=180,null=True))
# Group.add_to_class('description', models.CharField(max_length=180,null=True))
# Group.add_to_class('created_at', models.DateTimeField(auto_now_add=True, null=True))

# Group.add_to_class('created_by', models.CharField(max_length=180, null=True))

# Group.add_to_class('updated_at', models.DateTimeField(auto_now_add=True, null=True))
# Group.add_to_class('is_active', models.CharField(max_length=50,null=True, blank=True,default='1'))