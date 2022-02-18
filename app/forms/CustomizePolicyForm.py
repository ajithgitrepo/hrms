from django import forms  
from app.models.leave_request_model import LeaveRequest

# from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

class LeaveRequestForm(forms.ModelForm):  
   
   # marital_status = forms.ChoiceField(choices=Employee.MARITAL_CHOICES, widget=forms.RadioSelect())
    
    #date = forms.DateTimeField(widget=forms.widgets.DateTimeInput(format="%d/%m/%Y %H:%M:%S", attrs={'placeholder':"DD/MM/YY HH:MM:SS"}))
    class Meta:  
        model = LeaveRequest  
       # fields = "__all__",   "mobile_number",
        fields =("employee_id", "leave_type",  "reason", 'team_mailid', 'reason') #"role", "department") #"date_of_joining")
        readonly_fields = ['created', 'updated_at', 'is_active']
      
#     def __init__(self, *args, **kwargs): "from_date", "to_date",
#         super(LeaveRequestForm, self).__init__(*args, **kwargs)
#         self.fields[ 'from_date' ].input_formats = [ '%d-%m-%Y' ]
       # self.fields[ 'to_date' ].input_formats = [ '%d-%m-%Y' ]

#     def __init__(self, *args, **kwargs):
#         super(LeaveRequestForm, self).__init__(*args, **kwargs)
#         self.fields[ 'to_date' ].input_formats = [ '%d-%m-%Y' ]
        


   


