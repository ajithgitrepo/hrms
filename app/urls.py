# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from app import views 
#from app import emloyee_views 



urlpatterns = [
   
    #path('leave_request/', views.leave_request, name="leave_request"),
    # The home page
    path('', views.dashborad_view.index, name='home'),
    
    #path('roles', views.roles, name="roles"),
    
    #path('leave_request/', views.leave_request, name="leave_request"),
    
     
    # Employee 
    path('employees/', views.employee_view.employees, name="employees"),
    path('add_employee/', views.employee_view.add_employee, name="add_employee"),
    path('update_employee/<str:pk>/', views.employee_view.update_employee, name="update_employee"),
    path('delete_employee/<str:pk>/', views.employee_view.delete_employee, name="delete_employee"),
    path('snippets', views.snippets, name="snippets"),

    # Roles 
    path('roles/', views.role_view.roles, name="roles"),
    path('add_roles/', views.role_view.add_roles, name="add_roles"),
    path('update_role/<str:pk>/', views.role_view.update_role, name="update_role"),
    path('delete_role/<str:pk>/', views.role_view.delete_role, name="delete_role"),

    # Departments 
    path('departments/', views.department_view.departments, name="departments"),
    path('add_departments/', views.department_view.add_departments, name="add_departments"),
    path('update_department/<str:pk>/', views.department_view.update_department, name="update_department"),
    path('delete_department/<str:pk>/', views.department_view.delete_department, name="delete_department"),

    # leave_request 
    path('leave_request/', views.leave_request, name="leave_request"),
    path('add_leave_request/', views.add_leave_request, name="add_leave_request"),
    path('update_leave_request/<str:pk>/', views.update_leave_request, name="update_leave_request"),
    path('delete_leave_request/<str:pk>/', views.delete_leave_request, name="delete_leave_request"),
    path('leave_request_more_info', views.leave_request_more_info, name="leave_request_more_info"),

    # leave type / settings
    path('leave_types/', views.leave_type_view.index, name="leave_types"),
    path('add_leave_type/', views.leave_type_view.add_leave_type, name="add_leave_type"),
    path('edit_leave_type/<str:pk>/', views.leave_type_view.edit_leave_type, name="edit_leave_type"),
    path('change_status/<str:pk>/<str:val>/', views.leave_type_view.change_status, name="change_status"),

    #leave balance
    path('leave_balance/', views.leave_balance_view.index, name="leave_balance"),
    path('customize_leave_balance/<str:pk>/', views.leave_balance_view.customize_leave_balance, name="customize_leave_balance"),
    path('date_change/', views.leave_balance_view.date_change, name="date_change"),

    #onboard employee
    path('add_onboard_employee/', views.onboard_employee_view.add_onboard_employee, name="add_onboard_employee"),
    path('onboard_employees/', views.onboard_employee_view.onboard_employees, name="onboard_employees"),
    path('delete_onboard_employee/<str:pk>/', views.onboard_employee_view.delete_onboard_employee, name="delete_onboard_employee"),
    path('snippets_candidate_all_info', views.snippets_candidate_all_info, name="snippets_candidate_all_info"),
    path('send_offer_letter/', views.onboard_employee_view.send_offer_letter, name="send_offer_letter"),
    path('preview_offer_letter/', views.onboard_employee_view.preview_offer_letter, name="preview_offer_letter"),
    path('convert_to_emp/<str:pk>/', views.onboard_employee_view.convert_to_emp, name="convert_to_emp"),

    #Attendance
    path('check_in_attn/', views.attendance_view.check_in_attn, name="check_in_attn"),
    path('check_out_attn/', views.attendance_view.check_out_attn, name="check_out_attn"),
    path('attn_listview/', views.attendance_view.attn_listview, name="attn_listview"),
    path('search_listview/<str:pk>/<str:month>/', views.attendance_view.search_listview, name="search_listview"),
    path('export_excel/', views.attendance_view.export_excel, name="export_excel"),
    path('attn_calendarview/', views.attendance_view.attn_calendarview, name="attn_calendarview"),

    # Organization Files
    path('add_folder/', views.organization_files_view.add_folder, name="add_folder"),
    # path('organinzation_files/', views.organization_files_view.index, name="organinzation_files"),
    path('add_org_files/', views.organization_files_view.add_org_files, name="add_org_files"),
    path('delete_org_file/<str:pk>/', views.organization_files_view.delete_org_file, name="delete_org_file"),
    # Class based view
    path('organinzation_files/', views.organization_files_view.IndexView.as_view(), name="organinzation_files"),

    #Employee Files
    path('employee_files/', views.employee_files_view.IndexView.as_view(), name="employee_files"),
    path('add_emp_files/', views.employee_files_view.add_emp_files, name="add_emp_files"),
    path('delete_emp_file/<str:pk>/', views.employee_files_view.delete_emp_file, name="delete_emp_file"),

    #New Hires
    path('new_hires/', views.new_hires_view.index, name="new_hires"),
    path('birthdays/', views.new_hires_view.birthdays, name="birthdays"),
    path('get_birthday/', views.new_hires_view.get_birthday, name="get_birthday"),

    #Announcements
    path('announcements/', views.announcements_view.index, name="announcements"),
    path('add_announcements/', views.announcements_view.add_announcements, name="add_announcements"),
    path('announcement_view/<str:pk>/', views.announcements_view.announcement_view, name="announcement_view"),
    path('delete_announcement/<str:pk>/', views.announcements_view.delete_announcement, name="delete_announcement"),
    path('status_announcement/<str:pk>/<str:val>/', views.announcements_view.status_announcement, name="status_announcement"),

    path("unicorn/", include("django_unicorn.urls")),

   # path('emp', views.emp, name='emp'),
   # re_path(r'^.*\.*', views.emp, name='emp'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

    #re_path(r'^.*\.*', views.emp, name='emp'),
    #re_path(r'^.*\.*', views.emp, name='pages'),
   
    #path("emp/", views.emp, name='emp') 

]
