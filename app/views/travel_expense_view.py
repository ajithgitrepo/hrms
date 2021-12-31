
from app.models import exit_details_model
from app.models.onboard_employee_model import Onboard_Employee, Onboard_Work_Experience, Onboard_Education
from app.models.travel_request_model import Travel_Request_Detail
from app.models.travel_expense_model import Travel_Expense_Detail, Travel_Expense_More_Detail



from app.models.employee_model import Employee
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.TarvelExpense_DetailsForm import TarvelExpense_DetailForm
from django.conf import settings

#from app.forms import UserGroupForm  

# from app.models.employee_model import Onboard_Employee , 
# from app.models import Group 

#from app.models import Group 
from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
from django.db import connection
from datetime import datetime
import datetime

from django.utils import timezone

from app.views.travel_request_view import travel_request_details

#from app.models import QuillModel



@login_required(login_url="/login/")
def travel_expense_details(request):
    
    employee = Travel_Expense_Detail.objects.filter(is_active='1').order_by('-created_at')
    context = {'employees':employee}
    return render(request, "travel_expense_details/index.html", context)


def snippets_travel_details_travel_expense_more_all_info(request):
    
    id =    request.POST.get('trav_exp_id')
#     return HttpResponse(id)
    csrf =    request.POST.get('csrfmiddlewaretoken')
    
    final_list = Travel_Expense_More_Detail.objects.filter(travel_exp_id = id)
   
    jsondata = serializers.serialize('json', final_list)
 
    return HttpResponse(jsondata, content_type='application/json')
  


def add_travel_expense_details(request):  
    #return HttpResponse('working..') 
   # return render(request, "exit_details/add_exit_details.html")
    form = TarvelExpense_DetailForm()
   # return HttpResponse(form)
   # """
    if request.method == 'POST':
        form = TarvelExpense_DetailForm(request.POST)
        if  form.is_valid(): 
           # return HttpResponse('working..') 
            employee = request.POST.get('employee')
           
            travel = request.POST.get('travel')    
            
            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'
            # if not Asset_Detail.objects.filter( Q(employee=employee)).exists():
            obj = Travel_Expense_Detail.objects.create( 

            employee_id=employee, 
            travel_id=travel,
            created_at=created_at, updated_at=updated_at, is_active=is_active,

            ) 
               # return HttpResponse(employee)   
            obj.save()

            latest_id = Travel_Expense_Detail.objects.latest('id').id

           # return HttpResponse(latest_id)   

            # Expense
            description = request.POST.getlist('description')
            date = request.POST.getlist('date')
            ticket = request.POST.getlist('ticket')
            lodging = request.POST.getlist('lodging')
            boarding = request.POST.getlist('boarding')

            phone = request.POST.getlist('phone')
            local_conveyance = request.POST.getlist('local_conveyance')
            incidentals = request.POST.getlist('incidentals')
            others = request.POST.getlist('others')
            currency = request.POST.getlist('currency')
            
            c = min([len(description), len(date), len(ticket), len(lodging), len(boarding), len(phone), len(local_conveyance), len(incidentals), len(others), len(currency)])
                
            for i in range(c):
                  if description[i] and date[i] and ticket[i] and lodging[i] and boarding[i] and phone[i] and local_conveyance[i] and incidentals[i] and others[i] and currency[i] :
                        d = datetime.datetime.strptime(date[i], "%d-%m-%Y")
                        edu = Travel_Expense_More_Detail.objects.create(description=description[i], ticket=ticket[i], date= d.strftime('%Y-%m-%d'), lodging=lodging[i], boarding=boarding[i], phone= phone[i], local_conveyance= local_conveyance[i], incidentals= incidentals[i], others= others[i], currency= currency[i], employee_id  = employee, travel_exp_id = latest_id )

            messages.success(request, 'travel expense details was added ! ')
            return redirect(request.META.get('HTTP_REFERER'))
            # else: 
            #     employee = Employee.objects.all()
            #     context_role = {
            #             'employees': employee,
                     
            #             }
          
            #     context_role.update({"form":form})  
            #     messages.error(request, ' Asset Details Already Exists! ', context_role)
            #     context = {'form':form}
            #     return render(request, "travel_expense_details/add_asset_details.html", context)
             
    employee = Employee.objects.all()
    travel = Travel_Request_Detail.objects.all()
    travel_emp = Travel_Request_Detail.objects.filter(employee_id=request.user.emp_id)
    # print( travel)
   # print( employee)
    context_role = {
           'employees': employee,
           'travels': travel,
           'travel_emp':travel_emp,
       }
   
    #
   # tes = Group.objects.all()
    context_role.update({"form":form})
   # print(context_role)
    return render(request, "travel_expense_details/add_travel_expense.html",  context_role )
   
   
def delete_expense_details(request, pk):
   # return HttpResponse('working..')
    data = Travel_Expense_Detail.objects.get(id =pk)
    data.is_active = 0
    data.save()
    messages.error(request, 'travel expense was deleted! ')
    return redirect('travel_expense_details')

def snippets_travel_details_expense_all_info(request):
    
    travel_id =    request.POST.get('travel_id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
   
    final_list = Travel_Request_Detail.objects.filter(travel_id  = travel_id)
   
    jsondata = serializers.serialize('json', final_list)
 
    return HttpResponse(jsondata, content_type='application/json')

def travel_expense_approve(request):

    id = request.POST.get('id')
    value = request.POST.get('value')
    # print(value)

    data = Travel_Expense_Detail.objects.get(id = id)

    update = Travel_Expense_Detail.objects.filter(id=id).update(
        is_approved=value, 
        updated_by= request.user.emp_id,
        updated_at=timezone.now()
    )    

    return HttpResponse(1)


