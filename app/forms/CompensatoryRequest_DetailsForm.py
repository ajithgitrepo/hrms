from django import forms  
from app.models.compensatory_request_model import Compoensatory_Request_Detail

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

from django.conf import settings

from django.forms import ModelForm, Textarea

class CompensatoryRequest_DetailForm(forms.ModelForm):  
   

    class Meta:  
        model = Compoensatory_Request_Detail  
       # fields = "__all__",   "mobile_number",  "employee",
     
        fields = [  "worked_date",  "duration", "unit", "employee", ] #  "from_time",   "to_time",   ] #"role", "department") #"date_of_joining")
        readonly_fields = ['created', 'updated_at', 'is_active' ]

# "duration",  "expiry_date", "reason",

    def __init__(self, *args, **kwargs):
        super(CompensatoryRequest_DetailForm, self).__init__(*args, **kwargs)
        self.fields['worked_date'].required = True
        self.fields['worked_date'].widget.attrs['required'] = 'required'
        self.fields['worked_date'].error_messages = {'required': 'Worked Date is required'}
        self.fields['worked_date'].input_formats = [ '%d-%m-%Y' ]
      
        self.fields['unit'].required = True
        self.fields['unit'].widget.attrs['required'] = 'required'
        self.fields['unit'].error_messages = {'required': 'Unit is required'}  

        self.fields['duration'].required = True
        self.fields['duration'].widget.attrs['required'] = 'required'
        self.fields['duration'].error_messages = {'required': 'Duration is required'} 

      #   self.fields['from_time'].required = True
      #   self.fields['from_time'].widget.attrs['required'] = 'required'
      #   self.fields['from_time'].error_messages = {'required': 'Worked from time is required'}
        
      #   self.fields['to_time'].required = True
      #   self.fields['to_time'].widget.attrs['required'] = 'required'
      #   self.fields['to_time'].error_messages = {'required': 'Worked to time is required'}  

      #   self.fields['expiry_date'].required = True
      #   self.fields['expiry_date'].widget.attrs['required'] = 'required'
      #   self.fields['expiry_date'].error_messages = {'required': 'Expiry Date is required'}

      #   self.fields['reason'].required = True
      #   self.fields['reason'].widget.attrs['required'] = 'required'
      #   self.fields['reason'].error_messages = {'required': 'Reason is required'}  

        self.fields['employee'].required = True
        self.fields['employee'].widget.attrs['required'] = 'required'
        self.fields['employee'].error_messages = {'required': 'Employee is required'}
       
        
#     def __init__(self, *args, **kwargs):
#       super(CompensatoryRequest_DetailForm, self).__init__(*args, **kwargs)
#       self.fields[ 'worked_date' ].input_formats = [ '%d-%m-%Y' ]    



