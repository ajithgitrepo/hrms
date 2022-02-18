<<<<<<< HEAD
from django import forms  
from app.models.weekend_model import Weekend



from django.core.exceptions import ValidationError

class WeekendForm(forms.ModelForm):
#     OPTIONS = (
#            ("AUT", "Austria"),
#            ("DEU", "Germany"),
#            ("NLD", "Neitherlands"),
#        )
# #     week_off = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
#                                                  choices=OPTIONS)
#     week_off = forms.ModelMultipleChoiceField(queryset=Weekend.objects.none())
    class Meta:
        model = Weekend
       # fields = "__all__",   "mobile_number",
        fields = [ "week_starts_on", "week_ends_on" ]
        readonly_fields = ['created_at', 'updated_at', 'is_active']
#         widgets = {
#                   'week_off': ()
#               }

#         def __init__(self, all_companies, *args, **kwargs):
#                 super(WeekendForm, self).__init__(*args, **kwargs)
#                 self.fields['week_off'].queryset = all_companies
#

   


=======
from django import forms  
from app.models.weekend_model import Weekend



from django.core.exceptions import ValidationError

class WeekendForm(forms.ModelForm):
#     OPTIONS = (
#            ("AUT", "Austria"),
#            ("DEU", "Germany"),
#            ("NLD", "Neitherlands"),
#        )
# #     week_off = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
#                                                  choices=OPTIONS)
#     week_off = forms.ModelMultipleChoiceField(queryset=Weekend.objects.none())
    class Meta:
        model = Weekend
       # fields = "__all__",   "mobile_number",
        fields = [ "week_starts_on", "week_ends_on" ]
        readonly_fields = ['created_at', 'updated_at', 'is_active']
#         widgets = {
#                   'week_off': ()
#               }

#         def __init__(self, all_companies, *args, **kwargs):
#                 super(WeekendForm, self).__init__(*args, **kwargs)
#                 self.fields['week_off'].queryset = all_companies
#

   


>>>>>>> origin/hrms-09-02-2022
