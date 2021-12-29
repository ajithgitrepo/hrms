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
from app.forms.UserGroupForm import UserGroupForm
from django.utils import timezone
import datetime 
#from app.forms import UserGroupForm  

from app.models.role_model import Role 
# from app.models import Group 

# #from app.models import Group 
# from django.conf.urls import url
# from pprint import pprint
# from datetime import datetime
# from django.shortcuts import render
# from django.template import RequestContext
# from django.db.models import Q
# from datetime import datetime
from django.contrib.auth.models import Group
# from django.core import serializers
# from django.http import JsonResponse
# from django.db import connection
# import MySQLdb
# from itertools import chain
# from django.db.models import Prefetch


#from app.models import QuillModel



@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index' 

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

def roles(request):
    roles = Group.objects.filter(is_active='1')
    # print(roles);
    context = {'roles':roles}
    return render(request, "roles/index.html", context)
def add_roles(request):
    form = UserGroupForm()
    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            role_name = request.POST.get('name')
            role_type = request.POST.get('role_type')
            description = request.POST.get('description')
            # print(form.errors)
            # print(role_name)
            g1 = Group.objects.create(name=role_name, role_type=role_type, description=description)
            messages.success(request, role_name +' Role was created! ')
            return redirect('roles')
    # print(form.errors)
    context = {'form':form}
    return render(request, "roles/add_roles.html", context)
def update_role(request, pk):
    role = Group.objects.get(id=pk)
    form = UserGroupForm(instance=role)
    # print(role)
    if request.method == 'POST':
        form = UserGroupForm(request.POST, instance=role)
        if form.is_valid():
            role_name = request.POST.get('name')
            role.updated_at = timezone.now()
            role.save()
            form.save()
            messages.success(request, role_name +' Role was updated! ')
            return redirect('roles')
    context = {'form':form,'role':role}
    return render(request, "roles/update_role.html", context)
def delete_role(request, pk):
    # return HttpResponse('working..')
    data = Group.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.success(request, ' Role was deleted! ')
    return redirect('roles')