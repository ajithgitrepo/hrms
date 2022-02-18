from django import forms  
from app.models.manual_checkin_model import Manual_Checkin_Detail

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

from django.conf import settings

from django.forms import ModelForm, Textarea

class ManualChekinForm(forms.ModelForm):  
   
#     from_time = forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'))
#     to_time = forms.TimeField(widget=forms.TimeInput(format='%I:%M%p'))
#     TIME_INPUT_FORMATS = ['%I:%M %p',]
    class Meta:  
        model = Manual_Checkin_Detail  
        fields = [ "worked_date", "from_time", "to_time", "employee", ] #  "from_time",   "to_time",   ] #"role", "department") #"date_of_joining")
        readonly_fields = ['created', 'updated_at', 'is_active' ]



    def __init__(self, *args, **kwargs):
        super(ManualChekinForm, self).__init__(*args, **kwargs)
        self.fields['worked_date'].required = True
        self.fields['worked_date'].widget.attrs['required'] = 'required'
        self.fields['worked_date'].error_messages = {'required': 'Worked Date is required'}
        self.fields['worked_date'].input_formats = [ '%d-%m-%Y' ]


        self.fields['from_time'].required = True
        self.fields['from_time'].widget.attrs['required'] = 'required'
        self.fields['from_time'].error_messages = {'required': 'Worked from time is required'}
        self.fields['from_time'].input_formats = [ '%I:%M%p', ]
        
        self.fields['to_time'].required = True
        self.fields['to_time'].widget.attrs['required'] = 'required'
        self.fields['to_time'].error_messages = {'required': 'Worked to time is required'} 
        self.fields['to_time'].input_formats = [ '%I:%M%p', ]

      #   self.fields['reason'].required = True
      #   self.fields['reason'].widget.attrs['required'] = 'required'
      #   self.fields['reason'].error_messages = {'required': 'Reason is required'}  

        self.fields['employee'].required = True
        self.fields['employee'].widget.attrs['required'] = 'required'
        self.fields['employee'].error_messages = {'required': 'Employee is required'}
       
        
def __init__(self, *args, **kwargs):
      super(ManualChekinForm, self).__init__(*args, **kwargs)
      self.fields[ 'worked_date' ].input_formats = [ '%d-%m-%Y' ]    



