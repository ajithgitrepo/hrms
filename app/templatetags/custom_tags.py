from django import template
from django.http import request
from app.models.employee_model import Employee

register = template.Library()

  
@register.simple_tag(takes_context=True)
def role_name(context):
    request = context['request']
    role = Employee.objects.filter(role__is_active ='1',  employee_id= request.user.emp_id)
    return role[0].role.name