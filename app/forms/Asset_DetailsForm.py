from django import forms  
from app.models import Asset_Detail

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

from django.conf import settings

from django.forms import ModelForm, Textarea

class Asset_DetailForm(forms.ModelForm):  
   

    class Meta:  
        model = Asset_Detail  
       # fields = "__all__",   "mobile_number", 
     
        fields = [ "employee", "given_date",  "type_of_asset" ] #"role", "department") #"date_of_joining")
        readonly_fields = ['created', 'updated_at', 'is_active']
      
        
    def __init__(self, *args, **kwargs):
      super(Asset_DetailForm, self).__init__(*args, **kwargs)
      
      self.fields['employee'].required = True
      self.fields['employee'].widget.attrs['required'] = 'required'
      self.fields['employee'].error_messages = {'required': 'Employee is required'} 

      self.fields['type_of_asset'].required = True
      self.fields['type_of_asset'].widget.attrs['required'] = 'required'
      self.fields['type_of_asset'].error_messages = {'required': 'Type of asset is required'} 

      self.fields['given_date'].required = True
      self.fields['given_date'].widget.attrs['required'] = 'required'
      self.fields['given_date'].error_messages = {'required': 'Given Date is required'} 

      self.fields[ 'given_date' ].input_formats = [ '%d-%m-%Y' ]    



