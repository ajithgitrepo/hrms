# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.models import leave_type_model
from app.models import employee_model
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
from app.models.leave_balance_model import *
from app.models.customize_leave_balance import *
from app.models.department_model import *
from app.models.role_model import *
# from app.models.leave_balance_model import *
# from app.models import Group 

#from app.models import Group 
from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q, query
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
import json
from django.core import serializers
from django.core.mail import send_mail
from django.core import mail
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa  
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.conf import settings as django_settings
import os

from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage

#from app.models import QuillModel

@login_required(login_url="/login/")
def index(request):

    # # Child to parrent relationship
    # # balance = Leave_Balance.objects.filter(leave_type__is_active = '1',employee__is_active = "1")
  
    employees = Employee.objects.filter(is_active='1')

    types = Leave_Type.objects.filter(is_active='1')

    balance = Leave_Balance.objects.filter(is_active='1')

    balance_raw = Leave_Balance.objects.raw('SELECT lb.id,lb.balance,lt.name,lt.id as l_id,employee.first_name,employee.employee_id FROM employee LEFT JOIN leave_balance lb ON lb.employee_id = employee.employee_id JOIN leave_type lt ON lt.id = lb.leave_type_id where lb.is_active = "1" ')
   
    # print(balance_raw[0].first_name)

    # for balance in balance_raw:
    #     print(balance.first_name)

    res = []

    for bal in balance_raw:
        # res = str(res) + {'name':bal.first_name,'type':bal.name,'balance':str(bal.balance),'emp_id':bal.employee_id,'l_id': bal.l_id}
        res.append( {'name':bal.first_name,'type':bal.name,'balance':str(bal.balance),'emp_id':bal.employee_id,'l_id': bal.l_id} )
        # string_res = res.strip(' " " ') #.replace("'","")
        # Leave_Types =  eval(string_res)

    
    # print(res)
    

    context = {
        'employees': employees,
        'types': types,
        'balance': balance,
        'object':res,
        
    }

    return render(request, "leave_balance/index.html", context)
    
    # return HttpResponse(types)

    # data = Leave_Type.objects.all()

    # rows = Leave_Type.objects.raw('SELECT leave_type.id,name,type,unit,le.effective_after FROM leave_type LEFT JOIN leave_effective le ON le.leave_type_id = leave_type.id ')


def customize_leave_balance(request, pk):

    if request.method == 'POST':
        id = request.POST.getlist('leave_balance_id')
        date = request.POST.getlist('date')
        new_balance = request.POST.getlist('new_balance')
        reason = request.POST.getlist('reason')
        leave_type_id = request.POST.getlist('leave_type_id')
       
        iterate = 0
        for i in id:
            # print(new_balance[iterate])
            if new_balance[iterate] != '':
                # print(new_balance[iterate])
                # print(i)

                d = datetime.datetime.strptime(date[iterate], '%d-%m-%Y')
                final_date = d.strftime('%Y-%m-%d')

                # query = Customize_Leave_Balance.objects.filter(Q(leave_type_id=leave_type_id[iterate], employee_id=pk, date= final_date)).all()
                # print(query)

                if not Customize_Leave_Balance.objects.filter(Q(leave_type_id=leave_type_id[iterate], employee_id=pk, date= final_date)).exists():

                    type = Customize_Leave_Balance.objects.create(
                        balance=new_balance[iterate], 
                        date=final_date, 
                        created_at=datetime.datetime.now(),
                        updated_at=datetime.datetime.now(),
                        is_active="1",
                        customize_reason=reason[iterate],
                        device="web",
                        created_by_id=request.user.emp_id,
                        employee_id=pk,
                        leave_type_id=leave_type_id[iterate],

                    )

                else:

                    type = Customize_Leave_Balance.objects.filter(leave_type_id=leave_type_id[iterate], employee_id=pk, date= final_date).update(
                        balance=new_balance[iterate], 
                        created_at=datetime.datetime.now(),
                        updated_at=datetime.datetime.now(),
                        is_active="1",
                        customize_reason=reason[iterate],
                        device="web",
                        created_by_id=request.user.emp_id,

                    )

            iterate = iterate+1

        return redirect('leave_balance') 


    balance = Leave_Balance.objects.filter(is_active='1', employee_id=pk, employee__is_active = 1, leave_type__is_active = '1')

    # print(balance[0].employee.first_name)

    context = {
        'balance': balance,
    }

    return render(request, "leave_balance/customize/index.html", context)

   
def date_change(request):

    type = list(Leave_Effective.objects.filter(is_active='1',leave_type_id=request.GET.get('type_id')))
    employee = list(Employee.objects.filter(is_active='1',employee_id=request.GET.get('emp_id')))

    d = datetime.datetime.strptime(request.GET.get('date'), '%d-%m-%Y')
    final_date = d.strftime('%Y-%m-%d')

    customize_balance = list(Customize_Leave_Balance.objects.filter(leave_type_id=request.GET.get('type_id'), employee_id=request.GET.get('emp_id'), date=final_date ))
    # print(customize_balance)

    less_balance = list(Customize_Leave_Balance.objects.filter(leave_type_id=request.GET.get('type_id'), employee_id=request.GET.get('emp_id'), date__lt=final_date ).order_by('-date') ) 
    # print(less_balance)

    tmpJson = serializers.serialize("json",type)
    tmpObj = json.loads(tmpJson)

    empJson = serializers.serialize("json",employee)
    json2 = json.loads(empJson)

    balanceJson = serializers.serialize("json",customize_balance)
    json3 = json.loads(balanceJson)

    d_balanceJson = serializers.serialize("json",less_balance)
    json4 = json.loads(d_balanceJson)

    dict = {
        'type': tmpObj,
        'employee': json2,
        'customize_balance': json3,
        'less_balance': json4,
    }


    # return HttpResponse(json.dumps(dict))

    return HttpResponse( json.dumps(dict) )

    