from django import forms  
from app.models.travel_request_model import Travel_Request_Detail

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

from django.conf import settings

from django.forms import ModelForm, Textarea

class TarvelRequest_DetailForm(forms.ModelForm):  
   

    class Meta:  
        model = Travel_Request_Detail  
       # fields = "__all__",   "mobile_number",  "employee",
     
        fields = [ "place_of_visit", "employee", ]
        readonly_fields = ['created', 'updated_at', 'is_active' ]


    def __init__(self, *args, **kwargs):
        super(TarvelRequest_DetailForm, self).__init__(*args, **kwargs)
        self.fields['place_of_visit'].required = True
        self.fields['place_of_visit'].widget.attrs['required'] = 'required'
        self.fields['place_of_visit'].error_messages = {'required': 'Place of visit is required'}
        
        # self.fields['employee_department'].required = True
        # self.fields['employee_department'].widget.attrs['required'] = 'required'
        # self.fields['employee_department'].error_messages = {'required': 'Department is required'}  

        self.fields['employee'].required = True
        self.fields['employee'].widget.attrs['required'] = 'required'
        self.fields['employee'].error_messages = {'required': 'Employee is required'} 
       
        
#     def __init__(self, *args, **kwargs):
#       super(TarvelRequest_DetailForm, self).__init__(*args, **kwargs)
#       self.fields[ 'expected_date_of_depature' ].input_formats = [ '%d-%m-%Y' ]    



