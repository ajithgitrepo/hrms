<<<<<<< HEAD


from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.EmployeeForm import EmployeeForm
from app.models.department_model import Department 


from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
from app.models.reporting_to_model import Reporting
from django.contrib.auth.models import User

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
import MySQLdb
from itertools import chain
import datetime
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.contrib.auth.hashers import make_password, check_password



@login_required(login_url="/login/")
def index(request):
    
    employee = Employee.objects.select_related().filter(is_active='1', employee_id = 'Emp101')
    reporting = Reporting.objects.filter(employee__is_active = 1, reporting_id = 'Emp101')
    context = {
        'employees':employee,
        'reporting':reporting
    }

    # print(reporting[0].employee.first_name)

=======


from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.EmployeeForm import EmployeeForm
from app.models.department_model import Department 


from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
from app.models.reporting_to_model import Reporting
from django.contrib.auth.models import User

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
import MySQLdb
from itertools import chain
import datetime
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.contrib.auth.hashers import make_password, check_password



@login_required(login_url="/login/")
def index(request):
    
    employee = Employee.objects.select_related().filter(is_active='1', employee_id = 'Emp101')
    reporting = Reporting.objects.filter(employee__is_active = 1, reporting_id = 'Emp101')
    context = {
        'employees':employee,
        'reporting':reporting
    }

    # print(reporting[0].employee.first_name)

>>>>>>> origin/hrms-09-02-2022
    return render(request, "heirarchy_info/index.html", context)