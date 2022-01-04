from django import forms  
from app.models import Client

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

class ClientForm(forms.ModelForm):  
   

    class Meta:  
        model = Client  
       # fields = "__all__",   "mobile_number",
        fields =("client_name", "first_name", "last_name",  "email_id","mobile_number" )
        readonly_fields = ['created_at', 'updated_at', 'is_active' ]



