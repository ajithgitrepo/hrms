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
#from app.forms import UserGroupForm
from app.views.restriction_view import admin_only,role_name
from django.contrib.auth.models import User
# from app.models import Group

#from app.models import Group
from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q, manager
from django.utils import timezone
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
from django.db import connection
import MySQLdb
from itertools import chain
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta

from app.models.workhome_model import Workhome
from app.models.attendance_model import Attendance
from app.models.reporting_to_model import Reporting


from dateutil import relativedelta
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.core.files import File as DjangoFile
import os
from django.conf import settings


def workhome_approves(request):

    role = role_name(request)
    # print(role)
    if role == "Admin":
        workhome = Workhome.objects.filter(is_active=1)
    if role == "Manager":
        reporting_id=request.user.emp_id
        # print(reporting_id)
        reporting = Reporting.objects.filter(is_active=1 ,reporting_id=reporting_id).values('employee_id')
        # print(reporting)
        workhome = Workhome.objects.filter(is_active=1,employee_id__in=reporting)

    context = {'workhome_approves': workhome}
    return render(request, "workhome/approval.html", context)

def change_wfh_status(request):

    id = request.POST.get('id')
    value = request.POST.get('value')
    # print(value)

    data = Workhome.objects.get(id = id)

    update = Workhome.objects.filter(id=id).update(
        is_approved=value, 
        updated_by_id = request.user.emp_id,
        updated_at=timezone.now()
    )    
    # print(update)
    if update:
        start_date = datetime.strptime(str(data.start_date), "%Y-%m-%d")
        end_date = datetime.strptime(str(data.end_date), "%Y-%m-%d")
        # print(start_date)
        diff = abs((end_date-start_date).days)+1
        # print(diff)

        delta = end_date - start_date
        # print(delta)
        # print(value)
        first = True
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            print(day)
            # print(datetime.strftime(day, "%d-%m-%Y"))
            
            if value == '1':
                attn = Attendance.objects.filter(date=datetime.strftime(day, "%Y-%m-%d"), employee_id= data.employee_id).update(
                    is_wfh_approved=1, 
                    updated_at=timezone.now()
                )

            if value == '0' or value == '2':
                attn = Attendance.objects.filter(date=datetime.strftime(day, "%Y-%m-%d"), employee_id= data.employee_id).update(
                    is_wfh_approved=0, 
                    updated_at=timezone.now()
                )

        return HttpResponse(1)
    return HttpResponse(0)

    # return HttpResponse(1)


