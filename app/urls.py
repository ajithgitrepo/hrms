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
    
    # path('roles', views.roles, name="roles"),
    
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



   # path('emp', views.emp, name='emp'),
   # re_path(r'^.*\.*', views.emp, name='emp'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

    #re_path(r'^.*\.*', views.emp, name='emp'),
    #re_path(r'^.*\.*', views.emp, name='pages'),
   
    #path("emp/", views.emp, name='emp') 

]
