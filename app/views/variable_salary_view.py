
import imp
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from app.forms.VariablesalaryForm import VariablesalaryForm
from django.utils import timezone
import datetime 
#from app.forms import UserGroupForm  

from app.models.business_unit_model import Business_Unit 
from app.models.variable_salary_model import Variable_Salary

from django.contrib.auth.models import Group
from app.views.restriction_view import admin_only,role_name


@login_required(login_url="/login/")
@admin_only
def variable_salaries(request):
    #return HttpResponse('work')
    variable_salary = Variable_Salary.objects.filter(is_active='1')
    # print(departments);
    context = {'variable_salary':variable_salary}
    return render(request, "variable_salary/index.html", context)

@admin_only
def add_variable_salary(request):
    form = VariablesalaryForm()
    if request.method == 'POST':
        form = VariablesalaryForm(request.POST)
        if form.is_valid():
            name=request.POST.get('name')
            businessunit = request.POST.get('businessunit')
            description = request.POST.get('description')
            device = "web"
            # print(form.errors)
            # print(role_name)
            g1 = Variable_Salary.objects.create(name=name,businessunit=Business_Unit.objects.get(id=businessunit) if businessunit else None ,
                                                description=description, device=device)
            messages.success(request,' Variable Salary  was created! ')
            return redirect('variable_salaries')
    # print(form.errors)
    businessunits = Business_Unit.objects.filter(is_active=1)
    context = {'form':form,'businessunits':businessunits}
    return render(request, "variable_salary/add_variable_salary.html", context)

@admin_only
def delete_variable_salary(request, pk):
    # return HttpResponse('working..')
    data = Variable_Salary.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.success(request, ' Variable Salary was deleted! ')
    return redirect('variable_salaries')