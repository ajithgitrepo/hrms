from django import template
from django.http import request
from app.models.employee_model import Employee
import datetime,time

register = template.Library()

  
@register.simple_tag(takes_context=True)
def role_name(context):
    request = context['request']
    role = Employee.objects.filter(role__is_active ='1',  employee_id= request.user.emp_id)
    # print(role[0].role.name)
    return role[0].role.name


def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(ts))

register.filter(print_timestamp)

@register.simple_tag(takes_context=True)
def profile_pic(context):
    request = context['request']
    profile = Employee.objects.filter(role__is_active ='1',  employee_id= request.user.emp_id)
    return profile[0].profile