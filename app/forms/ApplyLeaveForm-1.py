from django import forms  
from app.models import LeaveRequest

from django.core.exceptions import ValidationError  

class Apply_Leave_Form(forms.ModelForm):  

    # input_types = ['%d-%m-%Y']
    # start_date = forms.DateField(input_types)
    # end_date = forms.DateField(input_types)

    from_date = forms.DateField(input_formats=['%d-%m-%Y'])
    to_date = forms.DateField(input_formats=['%d-%m-%Y'])
   
    class Meta:  
        model = LeaveRequest  
        fields =("employee_id","leave_type","from_date","to_date",) 

