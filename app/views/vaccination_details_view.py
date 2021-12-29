
from app.models import exit_details_model
from app.models.onboard_employee_model import Onboard_Employee, Onboard_Work_Experience, Onboard_Education
from app.models.vaccination_model import Vaccination_Detail
from app.models.employee_model import Employee
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.Vaccination_DetailsForm import Vaccination_DetailForm
from django.conf import settings
from itertools import chain
from django.db.models import Max, Subquery, OuterRef

# from app.forms import UserGroupForm

# from app.models.employee_model import Onboard_Employee ,
# from app.models import Group

# from app.models import Group
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
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage

from app.views.employee_view import employees

# from app.models import QuillModel


@login_required(login_url="/login/")

# def index(request):

#     context = {}
#     context['segment'] = 'index'

#     html_template = loader.get_template('index.html')
#     return render(html_template.render(context, request))

def vaccination_details(request):
    employee = Vaccination_Detail.objects.filter(is_active='1')
    context = {'employees': employee}
    return render(request, "vaccination_details/index.html", context)


def snippets_vaccinae_employee_all_info(request):

    roles = Group.objects.filter(is_active='1')
    emp_id = request.POST.get('emp_id')
    csrf = request.POST.get('csrfmiddlewaretoken')
    final_list = Employee.objects.filter(employee_id=emp_id).annotate(
        test=Subquery(Group.objects.filter(id=OuterRef('role')).values('role_type')))
    test = final_list.values_list('role', flat=True)

    locs = Vaccination_Detail.objects.filter(employee_id=emp_id,is_active='1')
    final_list_arr = list(chain(final_list, roles, locs))

    jsondata = serializers.serialize('json', final_list_arr)

#     emp_id = request.POST.get('emp_id')
#     csrf = request.POST.get('csrfmiddlewaretoken')

#     final_list = Vaccination_Detail.objects.filter(employee_id=emp_id)

#     jsondata = serializers.serialize('json', final_list)

    return HttpResponse(jsondata, content_type='application/json')


def add_vaccination_details(request):
    # return render(request, "vaccination_details/add_vaccination_details.html")
    form = Vaccination_DetailForm()

    if request.method == 'POST':
        form = Vaccination_DetailForm(request.POST)
        if form.is_valid():

            employee = request.POST.get('employee')

            if Vaccination_Detail.objects.filter( Q(employee=employee)).exists():
               employee = Employee.objects.all()
               context_role = {
                        'employees': employee,
                        #  'country': 'in'
                  }
               messages.success(request, 'Employee already exists ! ')   
               context_role.update({"form": form})

               return render(request, "vaccination_details/add_vaccination_details.html",  context_role)  

           # return HttpResponse(employee)

            vaccinated_status = request.POST.get('vaccinated_status')
          #  return HttpResponse(employee)
            vaccin_name = request.POST.get('vaccin_name')

            commends = request.POST.get('commends')

            vaccin_name = request.POST.get('vaccin_name')

            partial_vacci_date = request.POST.get('partial_vacci_date')
            if partial_vacci_date != "" and partial_vacci_date != None:
                # return HttpResponse(date)
                d = datetime.datetime.strptime(partial_vacci_date, '%d-%m-%Y')
                partial_vacci_date = d.strftime('%Y-%m-%d')
            else:
                partial_vacci_date = None

            date_of_vaccination = request.POST.get('date_of_vaccination')
            if date_of_vaccination != "" and date_of_vaccination != None:
                # return HttpResponse(date)
                d = datetime.datetime.strptime(date_of_vaccination, '%d-%m-%Y')
                date_of_vaccination = d.strftime('%Y-%m-%d')
            else:
                date_of_vaccination = None

            partci_doc_name = ""
            if request.FILES:

                upload = request.FILES['partial_url']

                if upload != None:
                    logoRoot = os.path.join(
                        settings.MEDIA_ROOT, 'vaccination_documents/')

                    logoRoot = logoRoot.replace("\\", "/")
                    partci_name = upload.name
                    realVar1 = partci_name.replace(" ", '')
                    partci_doc_name = realVar1
                    fs = FileSystemStorage(location=logoRoot)
                    # return HttpResponse(realVar)
                    file_name = fs.save(partci_doc_name, upload)
                    file_url = fs.url(file_name)

            vaccine_doc_name = ""
            if request.FILES:

                upload1 = request.POST.get('vaccine_url', False)
                # request.FILES['vaccine_url']
                if upload1 == False:
                    upload1 = request.FILES['vaccine_url']
              #  return HttpResponse(upload1)
                    if upload1 != None:
                        logoRoot = os.path.join(
                            settings.MEDIA_ROOT, 'vaccination_documents/')

                        logoRoot = logoRoot.replace("\\", "/")
                        vaccine_name = upload1.name
                        realVar = vaccine_name.replace(" ", '')
                        vaccine_doc_name = realVar
                        fs = FileSystemStorage(location=logoRoot)
                        file_name = fs.save(vaccine_doc_name, upload1)
                        file_url = fs.url(file_name)

            created_at = timezone.now()  # .strftime('%Y-%m-%d %H:%M:%S')
            updated_at = timezone.now()  # .strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'
            # if not Vaccination_Detail.objects.filter( Q(employee=employee)).exists():
            obj = Vaccination_Detail.objects.create(
                employee_id=employee,
                vaccinated_status=vaccinated_status,
                vaccin_name=vaccin_name,
                commends=commends,
                partial_vacci_date=partial_vacci_date,
                date_of_vaccination=date_of_vaccination,
                partial_url=partci_doc_name, vaccine_url=vaccine_doc_name,
                created_at=created_at, updated_at=updated_at, is_active=is_active,

            )
            # return HttpResponse(employee)
            obj.save()
            messages.success(request, 'vaccination details was added ! ')
            return redirect('vaccination_details')
            # else:
            #     employee = Employee.objects.all()
            #     context_role = {
            #             'employees': employee,

            #             }

            #     context_role.update({"form":form})
            #     messages.error(request, ' Asset Details Already Exists! ', context_role)
            #     context = {'form':form}
            #     return render(request, "asset_details/add_asset_details.html", context)

    employee = Employee.objects.all()
    context_role = {
        'employees': employee,
        #  'country': 'in'
    }
    context_role.update({"form": form})
    # print(context_role)
    return render(request, "vaccination_details/add_vaccination_details.html",  context_role)

def update_vaccination_details(request, pk):
     # return render(request, "vaccination_details/add_vaccination_details.html")
    form = Vaccination_DetailForm()
   # return HttpResponse('ok'); 
    if request.method == 'POST':
        form = Vaccination_DetailForm(request.POST)
        if form.is_valid():

            employee = request.POST.get('employee')
            
            vaccinated_status = request.POST.get('vaccinated_status')
          #  return HttpResponse(employee)
            vaccin_name = request.POST.get('vaccin_name')

            commends = request.POST.get('commends')

            vaccin_name = request.POST.get('vaccin_name')

            partial_vacci_date = request.POST.get('partial_vacci_date')
            if partial_vacci_date != "" and partial_vacci_date != "None" and partial_vacci_date != None:
                # return HttpResponse(date)
                d = datetime.datetime.strptime(partial_vacci_date, '%d-%m-%Y')
                partial_vacci_date = d.strftime('%Y-%m-%d')
            else:
                partial_vacci_date = None

            date_of_vaccination = request.POST.get('date_of_vaccination')
            #return HttpResponse(date_of_vaccination)
            if date_of_vaccination is not None and date_of_vaccination != "None" and date_of_vaccination != "":
               # return HttpResponse(date_of_vaccination)
                d = datetime.datetime.strptime(date_of_vaccination, '%d-%m-%Y')
                date_of_vaccination = d.strftime('%Y-%m-%d')
            else:
                 date_of_vaccination = None
                
                
          #  return HttpResponse(date_of_vaccination)
            partci_doc_name = ""
            if request.FILES:
                upload = request.POST.get('partial_url', False)
                  
                # request.FILES['vaccine_url']
                if upload == False:
                  upload = request.FILES['partial_url']
               # upload = request.FILES['partial_url']
                #return HttpResponse(upload)
                if upload != None and upload != "":
                   # return HttpResponse('upload')  
                    logoRoot = os.path.join(
                        settings.MEDIA_ROOT, 'vaccination_documents/')

                    logoRoot = logoRoot.replace("\\", "/")
                    partci_name = upload.name
                    realVar1 = partci_name.replace(" ", '')
                    partci_doc_name = realVar1
                    fs = FileSystemStorage(location=logoRoot)
                    # return HttpResponse(realVar)
                    file_name = fs.save(partci_doc_name, upload)
                    file_url = fs.url(file_name)

            vaccine_doc_name = ""
            if request.FILES:

                upload1 = request.POST.get('vaccine_url', False)
                # request.FILES['vaccine_url']
                if upload1 == False:
                    upload1 = request.FILES['vaccine_url']
              #  return HttpResponse(upload1)
                    if upload1 != None and upload != "":
                        logoRoot = os.path.join(
                            settings.MEDIA_ROOT, 'vaccination_documents/')

                        logoRoot = logoRoot.replace("\\", "/")
                        vaccine_name = upload1.name
                        realVar = vaccine_name.replace(" ", '')
                        vaccine_doc_name = realVar
                        fs = FileSystemStorage(location=logoRoot)
                        file_name = fs.save(vaccine_doc_name, upload1)
                        file_url = fs.url(file_name)

            updated_at = timezone.now()  # .strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'
            #  
            obj = Vaccination_Detail.objects.get(id=pk)
            obj.employee_id=employee
            obj.vaccinated_status=vaccinated_status
            obj.vaccin_name=vaccin_name
            obj.commends=commends
            obj.partial_vacci_date=partial_vacci_date
            obj.date_of_vaccination=date_of_vaccination
            if partci_doc_name is not None and partci_doc_name != "None" and partci_doc_name != "":
             obj.partial_url= partci_doc_name
            if vaccine_doc_name is not None and vaccine_doc_name != "None" and vaccine_doc_name != "":
             obj.vaccine_url=vaccine_doc_name
            obj.updated_at=updated_at
            obj.save()

          #  )
            # return HttpResponse(employee)
           # obj.save()
            messages.success(request, 'vaccination details was updated !')
            return redirect('vaccination_details')

    
    #return HttpResponse(employee1)
    employee = Employee.objects.filter(is_active=1)
    employee1 = Vaccination_Detail.objects.get(id = pk)
    context_role = {
        'employees_bk': employee,
        
        #  'country': 'in'
    }
    context_role.update({"form": form, 'vaccina': employee1})
    # print(context_role)
    return render(request, "vaccination_details/edit_vaccination_details.html",  context_role)


def delete_vaccine_details(request, pk):
   # return HttpResponse('working..')
    data = Vaccination_Detail.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.success(request, 'Vaccination details was deleted! ')
    # return redirect('asset_details')
    return redirect(request.META.get('HTTP_REFERER'))


def filter_vacciate_employees(request, status):

    val = 0
    if(status == "all"):
        val = ["Partially", "Fully", "Do not want to disclose", "Not vaccinated"]
    else:
        val = [status]

    employee = Vaccination_Detail.objects.filter(vaccinated_status__in=val,is_active='1')
    context = {'employees': employee}
    return render(request, "vaccination_details/index.html", context)
