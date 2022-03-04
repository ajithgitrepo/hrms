
import imp
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from app.forms.BusinessunitForm import BusinessunitForm
from django.utils import timezone
import datetime 
#from app.forms import UserGroupForm  

from app.models.business_unit_model import Business_Unit 
from app.models.department_model import Department

from django.contrib.auth.models import Group
from app.views.restriction_view import admin_only,role_name


@login_required(login_url="/login/")
@admin_only
def business_units(request):
    #return HttpResponse('work')
    business_unit = Business_Unit.objects.filter(is_active='1')
    # print(departments);
    context = {'business_unit':business_unit}
    return render(request, "business_unit/index.html", context)

@admin_only
def add_business_unit(request):
    form = BusinessunitForm()
    if request.method == 'POST':
        form = BusinessunitForm(request.POST)
        if form.is_valid():
            business_unit = request.POST.get('business_unit')
            company = request.POST.get('company')
            description = request.POST.get('description')
            device = "web"
            # print(form.errors)
            # print(role_name)
            g1 = Business_Unit.objects.create(business_unit=business_unit,
                                                company=Department.objects.get(id=company) if company else None, 
                                                description=description, device=device)
            messages.success(request,' Business Unit  was created! ')
            return redirect('business_units')
    # print(form.errors)
    company = Department.objects.filter(is_active=1)
    context = {'form':form,'company':company}
    return render(request, "business_unit/add_business_unit.html", context)

@admin_only
def delete_business_unit(request, pk):
    # return HttpResponse('working..')
    data = Business_Unit.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.success(request, ' Business Unit was deleted! ')
    return redirect('business_units')