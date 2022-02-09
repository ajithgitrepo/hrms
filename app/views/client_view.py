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
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.ClientForm import ClientForm

#from app.forms import UserGroupForm

from app.models.client_model import Client
from django.contrib.auth.models import User
from django.conf.urls import url
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.conf import settings
from django.core import serializers


def clients(request):
   # return HttpResponse("employee")
    clients = Client.objects.filter(is_active='1')

    context = {'clients': clients}
    return render(request, "client/index.html", context)


def add_client(request):

    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client_name = request.POST.get('client_name')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            mobile_number = request.POST.get('mobile_number')
            email_id = request.POST.get('email_id')
            phone = request.POST.get('phone')

            fax = request.POST.get('fax')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')

            pincode = request.POST.get('pincode')
            industry = request.POST.get('industry')
            company_size = request.POST.get('company_size')
            description = request.POST.get('description')

            
            g1 = Client.objects.create( client_name=client_name,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email_id=email_id,
                                        mobile_number=mobile_number,
                                        phone=phone,
                                        fax=fax,
                                        address=address,
                                        city=city,
                                        state=state,
                                        country=country,
                                        pincode=pincode,
                                        industry=industry,
                                        company_size=company_size,
                                        description=description)
            messages.success(request,' Client was created! ')
            return redirect('clients')

            
               
    context = {'form': form}
    return render(request, "client/add_client.html", context)


def update_client(request, pk):
    # return HttpResponse('working..')
    #role = Group.objects.get(id=pk)
    client = Client.objects.get(id=pk)
    form = ClientForm(instance=client)
    # print(role)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():

            client_name = request.POST.get('client_name')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            mobile_number = request.POST.get('mobile_number')
            email_id = request.POST.get('email_id')
            phone = request.POST.get('phone')

            fax = request.POST.get('fax')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')

            pincode = request.POST.get('pincode')
            industry = request.POST.get('industry')
            company_size = request.POST.get('company_size')
            description = request.POST.get('description')
            # return HttpResponse(pk)
            obj = Client.objects.filter(id=pk).update(client_name=client_name,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email_id=email_id,
                                        mobile_number=mobile_number,
                                        phone=phone,
                                        fax=fax,
                                        address=address,
                                        city=city,
                                        state=state,
                                        country=country,
                                        pincode=pincode,
                                        industry=industry,
                                        company_size=company_size,
                                        description=description)
            messages.success(request, ' Client was updated! ')
            return redirect('clients')

    context_role={"form": form, 'client': client}
    return render(request, "client/update_client.html", context_role)


def delete_client(request, pk):
    # return HttpResponse('working..')
    data = Client.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.success(request, 'Client was deleted! ')
    return redirect('clients')

def info(request):
     
    id =    request.POST.get('id')
    # print(id)
    csrf =    request.POST.get('csrfmiddlewaretoken')

    client = Client.objects.filter(id = id)
    
    # print(client[0].industry)
   
    jsondata = serializers.serialize('json', client)
    # print(jsondata)
 
    return HttpResponse(jsondata, content_type='application/json')