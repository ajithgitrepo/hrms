from django import forms  
from app.models.department_model import Department
from app.models.announcement_model import Announcement

from django.core.exceptions import ValidationError  

class AnnouncementForm(forms.ModelForm):  
   
    class Meta:  
        model = Announcement  
       # fields = "__all__",
        fields = [ "title","subject","expiry_date"] 
        readonly_fields = ['created_at', 'updated_at', 'is_active']
      

        


   


