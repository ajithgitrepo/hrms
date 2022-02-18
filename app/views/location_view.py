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
from app.forms.LocationForm import LocationForm
from django.utils import timezone
import datetime
from django.db.models import Q
#from app.forms import UserGroupForm  

from app.models.location_model import Location

from django.contrib.auth.models import Group

#from app.models import QuillModel


@login_required(login_url="/login/")


def locations(request):
    #return HttpResponse('work')
    locations = Location.objects.filter(is_active='1')
    context = {'locations':locations}
    return render(request, "location/index_location.html", context)

def add_location(request):
    form = LocationForm()
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = request.POST.get('location')
            description = request.POST.get('description')
            device = "web"
            # print(form.errors)
            # print(role_name)
            g1 = Location.objects.create(location=location, description=description, device=device)
            messages.success(request, location +' Department was created! ')
            return redirect('locations')
    # print(form.errors)
    context = {'form':form}
    return render(request, "location/add_location.html", context)

def update_location(request, pk):
    dept = Location.objects.get(id=pk)
    form = LocationForm(instance=dept)
    # print(role)
    if request.method == 'POST':

        form = LocationForm(request.POST, instance=dept)
        if form.is_valid():
            print('dsa')
            loc = request.POST.get('location')
            des = request.POST.get('description')
            dept.location = loc
            dept.description = des
            dept.updated_at = timezone.now()
            dept.save()
            messages.success(request, loc +' Location was updated! ')
            return redirect('locations')
    context = {'form':form,'location':dept}
    return render(request, "location/update_location.html", context)

def delete_location(request,pk):
    # return HttpResponse('working..')
    data = Location.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.success(request, ' Location was deleted! ')
    return redirect('locations')

def filter_location(request):
#     print('query')

    query = request.GET.get("location")
    print(query)
    if query =="":
        locations = Location.objects.filter(is_active='1')
    else:
        locations = Location.objects.filter(Q(location=query,is_active=1))

    context = {'locations':locations}
    return render(request, "location/index_location.html", context)

