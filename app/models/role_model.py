# -*- encoding: utf-8 -*-
""" 
Copyright (c) 2019 - present AppSeed.us 
"""

from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group

# Create your models here.

class Role(models.Model):

 id = models.AutoField(primary_key=True)
 Group.add_to_class('role_type', models.CharField(max_length=180,null=True))
 Group.add_to_class('description', models.CharField(max_length=180,null=True))
 Group.add_to_class('created_at', models.DateTimeField(auto_now_add=True, null=True))

 Group.add_to_class('created_by', models.CharField(max_length=180, null=True))

 Group.add_to_class('updated_at', models.DateTimeField(auto_now_add=True, null=True))
 Group.add_to_class('is_active', models.CharField(max_length=50,null=True, blank=True,default='1'))
    

 User.add_to_class('role', models.IntegerField(null=True, blank=True))
 User.add_to_class('emp_id', models.CharField(max_length=50,null=True, blank=True))
    
    

 