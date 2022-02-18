from django import forms  
from app.models.location_model import Location

from django.core.exceptions import ValidationError

class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
       # fields = "__all__",   "mobile_number",
        fields = [ "location" ]
        readonly_fields = ['created', 'updated_at', 'is_active']
      

        


   


