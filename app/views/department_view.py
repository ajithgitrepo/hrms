
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from app.forms.DepartmentForm import DepartmentForm
from django.utils import timezone
import datetime 
#from app.forms import UserGroupForm  

from app.models.department_model import Department 

from django.contrib.auth.models import Group
from app.views.restriction_view import admin_only,role_name


@login_required(login_url="/login/")
@admin_only
def departments(request):
    #return HttpResponse('work')
    departments = Department.objects.filter(is_active='1')
    # print(departments);
    context = {'departments':departments}
    return render(request, "department/index.html", context)

@admin_only
def add_departments(request):
    form = DepartmentForm()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept_name = request.POST.get('name')
            description = request.POST.get('description')
            device = "web"
            # print(form.errors)
            # print(role_name)
            g1 = Department.objects.create(name=dept_name, description=description, device=device)
            messages.success(request, dept_name +' Department was created! ')
            return redirect('departments')
    # print(form.errors)
    context = {'form':form}
    return render(request, "department/add_department.html", context)

@admin_only
def update_department(request, pk):
    dept = Department.objects.get(id=pk)
    form = DepartmentForm(instance=dept)
    # print(role)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            dept_name = request.POST.get('name')
            description = request.POST.get('description')
            dept.name = dept_name
            dept.description = description
            dept.updated_at = timezone.now()
            dept.save()
            form.save()
            messages.success(request, dept_name +' Department was updated! ')
            return redirect('departments')
    context = {'form':form,'department':dept}
    return render(request, "department/update_department.html", context)

@admin_only
def delete_department(request, pk):
    # return HttpResponse('working..')
    data = Department.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.success(request, ' Department was deleted! ')
    return redirect('depatments')