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
from django.utils import timezone
import datetime
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login

#from app.forms import UserGroupForm  

from app.models.weekend_model import Weekend
from app.forms.WeekendForm import WeekendForm

#from app.models import QuillModel


# @login_required(login_url="/login/")


def weekends(request):
    #return HttpResponse('work')
    weekends = Weekend.objects.filter(is_active='1')
    context = {'weekends':weekends}
    return render(request, "weekend/index_weekend.html", context)

def add_weekend(request):
    form = WeekendForm()
    if request.method == 'POST':
        form = WeekendForm(request.POST)
        if form.is_valid():
            week_starts_on = request.POST.get('week_starts_on')
            week_ends_on = request.POST.get('week_ends_on')
            week_off = request.POST.getlist('week_off')
#             print(week_off)

            device = "web"
            # print(form.errors)
            # print(role_name)
            g1 = Weekend.objects.create(week_starts_on=week_starts_on, week_ends_on=week_ends_on,week_off=week_off,device=device)
            messages.success(request,' Weekend was created! ')
            return redirect('weekends')
    # print(form.errors)
    context = {'form':form}
    return render(request, "weekend/add_weekend.html", context)

def update_weekend(request, pk):
    weekend = Weekend.objects.get(id=pk)
    form = WeekendForm(instance=weekend)

    if request.method == 'POST':
        form = WeekendForm(request.POST, instance=weekend)
        if form.is_valid():
                week_starts_on = request.POST.get('week_starts_on')
                week_ends_on = request.POST.get('week_ends_on')
                week_off = request.POST.getlist('week_off')
#                 print(week_off)

                device = "web"
                # print(form.errors)
                # print(role_name)
                g1 = Weekend.objects.filter(id=pk).update(week_starts_on=week_starts_on, week_ends_on=week_ends_on,week_off=week_off,device=device)
                messages.success(request,' Weekend was updated! ')
                return redirect('weekends')
        # print(form.errors)
    context = {'weekend':weekend}
    return render(request, "weekend/update_weekend.html", context)


def delete_weekend(request,pk):
    # return HttpResponse('working..')
    data = Weekend.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.error(request, ' Weekend was deleted! ')
    return redirect('weekends')