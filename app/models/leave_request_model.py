# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group

# Create your models here.

class LeaveRequest(models.Model):  
   
    id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=20, blank = False, null = False)  
    leave_type = models.CharField(max_length=30 , blank = False, null = False)
    from_date = models.DateField(blank = False, null = False)  
    to_date = models.DateField(blank = False, null = False)  
    total_days = models.CharField(max_length=12) 
    reason = models.TextField (blank = True, null = True)  
    is_approved = models.PositiveSmallIntegerField(default=0)
    is_rejected = models.PositiveSmallIntegerField(default=0) 

    team_mailid = models.CharField(max_length=250 , blank = True, null = True)

    action_by = models.CharField (max_length=30,blank = True, null = True)  
    
    added_by = models.CharField(max_length=30,blank = True, null = True) 
    updated_by = models.CharField(max_length=30,blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True)  

      
    class Meta:  
        db_table = "leave_request"  

   # self.fields[ 'dob' ].input_formats = [ '%Y-%m-%d' ]

# Group.add_to_class('role_type', models.CharField(max_length=180,null=True))
# Group.add_to_class('description', models.CharField(max_length=180,null=True))
# Group.add_to_class('created_at', models.DateTimeField(auto_now_add=True, null=True))

# Group.add_to_class('created_by', models.CharField(max_length=180, null=True))

# Group.add_to_class('updated_at', models.DateTimeField(auto_now_add=True, null=True))
# Group.add_to_class('is_active', models.CharField(max_length=50,null=True, blank=True,default='1'))