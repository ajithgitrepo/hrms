from django import forms  
from app.models.holiday_details_model import Holiday_Detail

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

from django.conf import settings



class Holiday_DetailsForm(forms.ModelForm):  
   

    class Meta:  
        model = Holiday_Detail  
       # fields = "__all__",   "mobile_number", 
     
        fields = [ 'holiday_name', 'date']#"role", "department") #"date_of_joining")
        readonly_fields = ['created', 'updated_at', 'is_active']

    def __init__(self, *args, **kwargs):
        super(Holiday_DetailsForm, self).__init__(*args, **kwargs)
        self.fields['holiday_name'].required = True
        self.fields['holiday_name'].widget.attrs['required'] = 'required'
        self.fields['holiday_name'].error_messages = {'required': 'Holiday name is required'}  
        self.fields[ 'date' ].input_formats = [ '%d-%m-%Y' ] 
        
#     def __init__(self, *args, **kwargs):
#      super(Holiday_DetailsForm, self).__init__(*args, **kwargs)
#         



