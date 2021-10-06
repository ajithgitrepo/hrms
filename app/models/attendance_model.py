
from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group
from app.models.department_model import Department 
from app.models.employee_model import *

class Attendance(models.Model):  
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    employee = models.ForeignKey(Employee, blank=True, null=True, related_name='employee_id_attendance', on_delete= models.SET_NULL)
    is_present = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    is_leave = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    checkin_time = models.TimeField(blank=True, null=True)
    checkout_time = models.TimeField(blank=True, null=True)
    is_leave_approved = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    leave_approved_by = models.ForeignKey(Employee, blank=True, null=True, related_name='approved_by_attendance', on_delete= models.SET_NULL)
    is_active = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True,blank=True, null=True,)
    updated_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)

    class Meta:  
        db_table = "attendance" 