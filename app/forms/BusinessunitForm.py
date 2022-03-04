from django import forms  
from app.models.business_unit_model import Business_Unit

from django.core.exceptions import ValidationError  

class BusinessunitForm(forms.ModelForm):  
   
    class Meta:  
        model = Business_Unit  
       # fields = "__all__",   "mobile_number",
        fields = [ "business_unit" ] #"role", "department") #"date_of_joining")
        readonly_fields = ['created', 'updated_at', 'is_active']
      

        


   


