
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.EmployeeForm import EmployeeForm
from app.models.department_model import Department
from app.views.employee_view import employees
from app.views.restriction_view import admin_only,role_name
#from app.forms import UserGroupForm

from app.models.employee_model import Employee, Work_Experience, Education, Dependent
from app.models.reporting_to_model import Reporting
from django.contrib.auth.models import User
# from app.models import Group

#from app.models import Group
from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q, manager
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
from django.db import connection
import MySQLdb
from itertools import chain
import datetime
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.contrib.auth.hashers import make_password, check_password

from app.models.employee_model import Employee
from app.models.client_model import Client
from app.models.project_model import Project
from app.forms.ProjectForm import ProjectForm



from dateutil import relativedelta
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.core.files import File as DjangoFile
import os
import datetime
from django.conf import settings



def projects(request):
   # return HttpResponse("employee")
    project = Project.objects.filter(is_active='1')

    context = {'projects': project}
    return render(request, "project/index.html", context)


def add_project(request):

    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            # print(request.POST.get('project_client'))
            project_name = request.POST.get('project_name')
            project_client = request.POST.get('project_client')
            # project_head = request.POST.get('project_head')
            project_manager = request.POST.get('project_manager')
            project_users = request.POST.getlist('project_users')
            project_users.append(project_manager)
            # print(project_users)
            project_cost = request.POST.get('project_cost')
            project_description = request.POST.get('project_description')

           
            obj = Project.objects.create(     project_name=project_name,
                                              project_client=Client.objects.get(id = project_client) if project_client else None, 
                                            #   project_head=Employee.objects.get(employee_id = project_head) if project_head else None, 
                                              project_manager=Employee.objects.get(employee_id = project_manager) if project_manager else None,
                                              project_users=project_users,
                                              project_cost=project_cost,
                                              project_description=project_description,                                             
                                         )
            messages.success(request,' Project was created! ')
            return redirect('projects')  

    client = Client.objects.select_related().filter(is_active='1')
    # hr = Employee.objects.filter(is_active='1',role_id='2')
    manager = Employee.objects.filter(is_active='1', role__name='Manager')
    employee = Employee.objects.filter(is_active='1', role__name='Associate')

                                                         
    context = {'form': form,'clients':client, 'managers':manager, 'employees':employee}
    return render(request, "project/add_project.html", context)

def update_project(request, pk):
    
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project_name = request.POST.get('project_name')
            project_client = request.POST.get('project_client')
            project_head = request.POST.get('project_head')
            project_manager = request.POST.get('project_manager')
            project_users = request.POST.getlist('project_users')
            project_users.append(project_manager)
            
            project_cost = request.POST.get('project_cost')
            project_description = request.POST.get('project_description')
            obj = Project.objects.filter(id=pk).update( 
                                              project_name=project_name,
                                              project_client=project_client, 
                                            #   project_head=Employee.objects.get(employee_id = project_head) if project_head else None, 
                                              project_manager=Employee.objects.get(employee_id = project_manager) if project_manager else None,
                                              project_users=project_users,
                                              project_cost=project_cost,
                                              project_description=project_description,
                                                                 )           
            messages.success(request, ' Project was updated! ')
            return redirect('projects')
    client = Client.objects.select_related().filter(is_active='1')
    # hr = Employee.objects.filter(is_active='1',role_id='2')
    manager = Employee.objects.filter(is_active='1', role__name='Manager')
    employee = Employee.objects.filter(is_active='1', role__name='Associate')
    # print(employee)
            
    context_role = {'form':form,'project':project,'clients':client, 'managers':manager, 'employees':employee}
    return render(request, "project/update_project.html", context_role)


def delete_project(request, pk):
    # return HttpResponse('working..')
    data = Project.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.success(request, 'Project was deleted! ')
    return redirect('projects')