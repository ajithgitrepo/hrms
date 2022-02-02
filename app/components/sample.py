from django_unicorn.components import UnicornView

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
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from app.models.attendance_model import Attendance 
from django.contrib.auth.models import Group

class SampleView(UnicornView):
    def attn_check_in(self):
        myDate = datetime.now()
        if not Attendance.objects.filter(Q(employee_id=self.request.user.emp_id, date=myDate, checkin_time__isnull=False)).exists():
            insert = Attendance.objects.create(date=myDate, checkin_time=datetime.now().strftime('%H:%M:%S'), employee_id= self.request.user.emp_id)
            self.request.session['checkin_session'] = datetime.now().strftime('%H:%M:%S')
            messages.success(self.request,' Checked in successfully ')
            pass
        else:
            update = Attendance.objects.filter(date=myDate, employee_id= self.request.user.emp_id ).update(
                updated_at = datetime.now(),
            )
        self.request.session['checkin_session'] = datetime.now().strftime('%H:%M:%S')
        # print(self.request.session['checkin_session'])
      
        pass 
   
    def attn_check_out(self):
        myDate = datetime.now()
        if Attendance.objects.filter(Q(employee_id=self.request.user.emp_id, date=myDate, checkin_time__isnull=False)).exists():
            update = Attendance.objects.filter(date=myDate, employee_id= self.request.user.emp_id ).update(
                checkout_time = datetime.now().strftime('%H:%M:%S'),
                updated_at = datetime.now(),
            )
            del self.request.session['checkin_session']
            messages.success(self.request,' Checked out successfully ')
            pass

        else:
            del self.request.session['checkin_session']
            messages.success(self.request,' Checked out successfully ')
            pass

    