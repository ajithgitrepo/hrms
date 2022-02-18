<<<<<<< HEAD
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from app.models.employee_model import Employee
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from app.forms.AnnouncementsForm import AnnouncementForm
from django.utils import timezone
import datetime 
#from app.forms import UserGroupForm  

from app.models.department_model import Department
from app.models.announcement_model import Announcement 

from django.contrib.auth.models import Group
import os
from django.conf import settings
from django.db.models import Q

#from app.models import QuillModel


@login_required(login_url="/login/")
def index(request):
    
    #Hr Login
    announcements = Announcement.objects.filter(added_by__is_active = 1, created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30)).order_by('-created_at')
    # print(announcements)

    #Employee Login
    # employee = Employee.objects.filter(is_active='1', employee_id = request.user.emp_id)
    # announcements = Announcement.objects.filter( Q(department_id= employee[0].department_id) | Q(department_id=None), is_active ='1', added_by__is_active = 1, created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30))
   
    context = {'announcements':announcements}
    return render(request, "announcements/index.html", context)

def add_announcements(request):
    form = AnnouncementForm()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            subject = request.POST.get('subject')
            expiry_date = request.POST.get('expiry_date')
            department = request.POST.get('department')

            if department == 'all':
                dept = None
                
            else:
                dept = department

            d2 = datetime.datetime.strptime(expiry_date, "%Y-%m-%d")
            expiry=d2.strftime('%Y-%m-%d')

            current_date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            
            if len(request.FILES) != 0:
                name = os.path.splitext(str(request.FILES['attachment']))[0]
                extesion = os.path.splitext(str(request.FILES['attachment']))[1]
                handle_uploaded_file(request.FILES['attachment'], current_date_time)
                file_name = name+"-"+current_date_time+""+extesion
            else:
                file_name = None

            insert = Announcement.objects.create(title=title, subject=subject, expiry_date=expiry, device = 'web', added_by_id= request.user.emp_id, updated_by_id= request.user.emp_id, department_id = dept, attachment = file_name  )
            messages.success(request, title +' Announcement was created! ')
            return redirect('announcements')

    
    departments = Department.objects.filter(is_active='1')
    context = {
        'form':form,
        'department':departments,
    }
    return render(request, "announcements/add_announcements.html", context)



def delete_announcement(request, pk):
    # return HttpResponse('working..')
    data = Announcement.objects.get(id=pk)
    data.delete()
    messages.success(request, ' Announcement was deleted! ')
    return redirect('announcements')


def announcement_view(request, pk):
    announcements = Announcement.objects.filter( Q(department__is_active= 1) | Q(department_id=None), id=pk, added_by__is_active = 1 )
    # print(announcements[0].department.name)
    context = {'announcements':announcements}
    return render(request, "announcements/announcement_view.html", context)


def handle_uploaded_file(f, current_date_time):
    name = os.path.splitext(str(f))[0]
    extesion = os.path.splitext(str(f))[1]
    file_name = name+"-"+current_date_time+""+extesion
   
    file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'announcements')

    with open(os.path.join(file_upload_dir, file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def status_announcement(request, pk, val):
    # return HttpResponse('working..')
    data = Announcement.objects.get(id=pk)
    data.is_active = val
    data.save()
    messages.success(request, ' Announcement status was changed! ')
=======
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from app.models.employee_model import Employee
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from app.forms.AnnouncementsForm import AnnouncementForm
from django.utils import timezone
import datetime 
#from app.forms import UserGroupForm  

from app.models.department_model import Department
from app.models.announcement_model import Announcement 

from django.contrib.auth.models import Group
import os
from django.conf import settings
from django.db.models import Q

#from app.models import QuillModel


@login_required(login_url="/login/")
def index(request):
    
    #Hr Login
    announcements = Announcement.objects.filter(added_by__is_active = 1, created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30)).order_by('-created_at')
    # print(announcements)

    #Employee Login
    # employee = Employee.objects.filter(is_active='1', employee_id = request.user.emp_id)
    # announcements = Announcement.objects.filter( Q(department_id= employee[0].department_id) | Q(department_id=None), is_active ='1', added_by__is_active = 1, created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30))
   
    context = {'announcements':announcements}
    return render(request, "announcements/index.html", context)

def add_announcements(request):
    form = AnnouncementForm()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            subject = request.POST.get('subject')
            expiry_date = request.POST.get('expiry_date')
            department = request.POST.get('department')

            if department == 'all':
                dept = None
                
            else:
                dept = department

            d2 = datetime.datetime.strptime(expiry_date, "%Y-%m-%d")
            expiry=d2.strftime('%Y-%m-%d')

            current_date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            
            if len(request.FILES) != 0:
                name = os.path.splitext(str(request.FILES['attachment']))[0]
                extesion = os.path.splitext(str(request.FILES['attachment']))[1]
                handle_uploaded_file(request.FILES['attachment'], current_date_time)
                file_name = name+"-"+current_date_time+""+extesion
            else:
                file_name = None

            insert = Announcement.objects.create(title=title, subject=subject, expiry_date=expiry, device = 'web', added_by_id= request.user.emp_id, updated_by_id= request.user.emp_id, department_id = dept, attachment = file_name  )
            messages.success(request, title +' Announcement was created! ')
            return redirect('announcements')

    
    departments = Department.objects.filter(is_active='1')
    context = {
        'form':form,
        'department':departments,
    }
    return render(request, "announcements/add_announcements.html", context)



def delete_announcement(request, pk):
    # return HttpResponse('working..')
    data = Announcement.objects.get(id=pk)
    data.delete()
    messages.success(request, ' Announcement was deleted! ')
    return redirect('announcements')


def announcement_view(request, pk):
    announcements = Announcement.objects.filter( Q(department__is_active= 1) | Q(department_id=None), id=pk, added_by__is_active = 1 )
    # print(announcements[0].department.name)
    context = {'announcements':announcements}
    return render(request, "announcements/announcement_view.html", context)


def handle_uploaded_file(f, current_date_time):
    name = os.path.splitext(str(f))[0]
    extesion = os.path.splitext(str(f))[1]
    file_name = name+"-"+current_date_time+""+extesion
   
    file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'announcements')

    with open(os.path.join(file_upload_dir, file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def status_announcement(request, pk, val):
    # return HttpResponse('working..')
    data = Announcement.objects.get(id=pk)
    data.is_active = val
    data.save()
    messages.success(request, ' Announcement status was changed! ')
>>>>>>> origin/hrms-09-02-2022
    return redirect('announcements')