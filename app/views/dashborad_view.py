# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.views.employee_view import employees
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.EmployeeForm import EmployeeForm 
from app.forms.LeaveTypeForm import LeaveTypeForm

#from app.forms import UserGroupForm  

from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
from app.models.leave_type_model import * 
from app.models.leave_balance import *
from app.models.department_model import *
from app.models.role_model import *
# from app.models.leave_balance_model import *
# from app.models import Group 

#from app.models import Group 
from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
import MySQLdb
from itertools import chain
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
import datetime
from django.db import connection,transaction
from django.db.models import F

#from app.models import QuillModel


@login_required(login_url="/login/")
def index(request):

    context = {}
    context['segment'] = 'index' 

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

    
