from django.db import models
from django.contrib.auth.models import User 
from app.models.project_model import *
from app.models.employee_model import *

class TimeLogs(models.Model): 
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    project = models.ForeignKey(Project, max_length=50, blank=False, related_name='timelog_project', null=True, on_delete= models.SET_NULL)
    employee = models.ForeignKey(Employee, max_length=50, blank=False, related_name='timelog_employee', null=True, on_delete= models.SET_NULL)
    working_on = models.CharField(max_length=255 , blank = False, null = False)
    working_on = models.TextField(blank = True, null = True)
    decription = models.TextField(blank = True, null = True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_active = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True,blank=True, null=True,)
    updated_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)

    class Meta:  
        db_table = "timelogs"  