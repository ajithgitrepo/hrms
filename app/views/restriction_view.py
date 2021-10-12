# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from app.forms.DepartmentForm import DepartmentForm
from django.utils import timezone
import datetime 
#from app.forms import UserGroupForm  

from app.models.department_model import Department 
from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
from django.contrib.auth.models import Group


def admin_only(function):
 
    def _inner(request, *args, **kwargs):
        role = Employee.objects.filter(role__is_active ='1', employee_id = request.user.emp_id )
        # print(role[0].role.name)
        if not role[0].role.name == 'Admin':
            return render(request, "page-403.html")  
        # if not request.user.is_superuser:
        #     raise PermissionDenied             
        return function(request, *args, **kwargs)
    return _inner

def role_name(request):
    role = Employee.objects.filter(role__is_active ='1', employee_id = request.user.emp_id )
    return role[0].role.name