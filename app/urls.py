
from django.urls import path, re_path, include
from app import views 
from app.views.restriction_view import admin_only,role_name

urlpatterns = [
   
    #Home page
    path('', views.dashborad_view.index, name='home'),
  
    #Self Service
    path('profile/', views.self_service_view.profile, name="profile"),
    path('attendance/', views.self_service_view.attendance, name="attendance"),
    path('filter_attendance/<str:month>/', views.self_service_view.filter_attendance, name="filter_attendance"),
    path('files/', views.self_service_view.files, name="files"),
    path('add_files/', views.self_service_view.add_files, name="add_files"),
    path('assets/', views.self_service_view.assets, name="assets"),
    path('add_asset/', views.self_service_view.add_asset, name="add_asset"),
    path('leave_tracker/', views.self_service_view.leave_tracker, name="leave_tracker"),
    path('apply_leave/', views.self_service_view.apply_leave, name="apply_leave"),
    path('leave/<str:leave>/', views.self_service_view.leave, name="leave"),
    path('self_travel_request/', views.self_service_view.self_travel_request, name="self_travel_request"),
    path('add_self_travel_request/', views.self_service_view.add_self_travel_request, name="add_self_travel_request"),
    path('delete_travel_request/<str:pk>/', views.self_service_view.delete_travel_request, name="delete_travel_request"),
    path('self_travel_expense/', views.self_service_view.self_travel_expense, name="self_travel_expense"),
    path('compensatory_request/', views.self_service_view.compensatory_request, name="compensatory_request"),
    path('add_compensatory_request/', views.self_service_view.add_compensatory_request, name="add_compensatory_request"),
    # path('add_self_travel_expense/', views.self_service_view.add_self_travel_expense, name="add_self_travel_expense"),
    # path('delete_travel_expense/<str:pk>/', views.self_service_view.delete_travel_expense, name="delete_travel_expense"),

    # Employee 
    path('employees/', views.employee_view.employees, name="employees"),
    path('add_employee/', views.employee_view.add_employee, name="add_employee"),
    path('update_employee/<str:pk>/', views.employee_view.update_employee, name="update_employee"),
    path('delete_employee/<str:pk>/', views.employee_view.delete_employee, name="delete_employee"),
    
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
    path('change_leave_status/', views.leave_request_view.change_leave_status, name="change_leave_status"),
   
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
    path('show_cal_view', views.attendance_view.show_cal_view, name='show_cal_view'),
    path('show_attn_time', views.attendance_view.show_attn_time, name='show_attn_time'),
    path('search_attn_time', views.attendance_view.search_attn_time, name='search_attn_time'),
    path('search_attn_date', views.attendance_view.search_attn_date, name='search_attn_date'),
    path('attn_tableview/', views.attendance_view.attn_tableview, name='attn_tableview'),
    path('search_tableview/<str:pk>/<str:month>/', views.attendance_view.search_tableview, name="search_tableview"),

    # Organization Files
    path('add_folder/', views.organization_files_view.add_folder, name="add_folder"),
    # path('organinzation_files/', views.organization_files_view.index, name="organinzation_files"),
    path('add_org_files/', views.organization_files_view.add_org_files, name="add_org_files"),
    path('delete_org_file/<str:pk>/', views.organization_files_view.delete_org_file, name="delete_org_file"),
    # Class based view
    path('organinzation_files/', admin_only(views.organization_files_view.IndexView.as_view()), name="organinzation_files"),

    #Employee Files
    path('employee_files/', admin_only(views.employee_files_view.IndexView.as_view()), name="employee_files"),
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

    # Calender
    path('calendar/', views.calendar_details_view.calendar, name='calendar'),
    path('add_event',views.calendar_details_view.add_event, name='add_event'),
    path('update/', views.calendar_details_view.update, name='update'),
    path('remove', views.calendar_details_view.remove, name='remove'),
    path('all_events', views.calendar_details_view.all_events, name='all_events'),

    # Travel Expenses
    path('travel_expense_details/', views.travel_expense_view.travel_expense_details, name="travel_expense_details"),
    path('add_travel_expense_details/', views.travel_expense_view.add_travel_expense_details, name="add_travel_expense_details"),
    path('snippets_travel_details_travel_expense_more_all_info', views.travel_expense_view.snippets_travel_details_travel_expense_more_all_info, name="snippets_travel_details_travel_expense_more_all_info"),
    path('delete_expense_details/<str:pk>/', views.travel_expense_view.delete_expense_details, name="delete_expense_details"),
   
    # Travel Request
    path('travel_request_details/', views.travel_request_view.travel_request_details, name="travel_request_details"),
    path('add_travel_request_details', views.travel_request_view.add_travel_request_details, name="add_travel_request_details"),
    path('delete_asset_details/<str:pk>/', views.travel_request_view.delete_asset_details, name="delete_asset_details"),
    path('snippets_travel_details_employee_all_info', views.travel_request_view.snippets_travel_details_employee_all_info, name="snippets_travel_details_employee_all_info"),
    
    # Compensatory Request
    path('compensatory_request_details/', views.compensatory_request_view.compensatory_request_details, name="compensatory_request_details"),
    path('add_compensatory_request_details/', views.compensatory_request_view.add_compensatory_request_details, name="add_compensatory_request_details"),
    path('delete_compensatory_details/<str:pk>/', views.compensatory_request_view.delete_compensatory_details, name="delete_compensatory_details"),
    path('snippets_compensatory_details_employee_all_info', views.compensatory_request_view.snippets_compensatory_details_employee_all_info, name="snippets_compensatory_details_employee_all_info"),
    path('compensatory_request_status/', views.compensatory_request_view.compensatory_request_status, name="compensatory_request_status"),

    # Asset Details
    path('asset_details/', views.asset_deatails_view.asset_details, name="asset_details"),
    path('add_asset_details', views.asset_deatails_view.add_asset_details, name="add_asset_details"),
    path('delete_asset_details/<str:pk>/', views.asset_deatails_view.delete_asset_details, name="delete_asset_details"),
    path('snippets_asset_all_info', views.asset_deatails_view.snippets_asset_all_info, name="snippets_asset_all_info"),
    
    # Holiday Details
    path('holiday_details/', views.holiday_details_view.holiday_details, name="holiday_details"),
    path('add_holiday_details', views.holiday_details_view.add_holiday_details, name="add_holiday_details"),
    path('delete_holiday_details/<str:pk>/', views.holiday_details_view.delete_holiday_details, name="delete_holiday_details"),
    
    # Exit Details
    path('exit_details/', views.exit_deatails_view.exit_details, name="exit_details"),
    path('add_exit_details', views.exit_deatails_view.add_exit_details, name="add_exit_details"),
    path('delete_employee_exit_details/<str:pk>/', views.exit_deatails_view.delete_employee_exit_details, name="delete_employee_exit_details"),
    path('snippets_exit_employee_all_info', views.snippets_exit_employee_all_info, name="snippets_exit_employee_all_info"),
    
    # Organization Tree
    path('organization_tree/', views.heirarchy_view.index, name="organization_tree"),

    #Task
    path('tasks/', views.task_view.tasks, name="tasks"),
    path('add_task/', views.task_view.add_task, name="add_task"),
    path('delete_task/<str:pk>/', views.task_view.delete_task, name="delete_task"),
    path('update_task/<str:pk>/', views.task_view.update_task, name="update_task"),
    path('search/', views.task_view.search, name="search"),

    # Location
    path('locations/', views.location_view.locations, name="locations"),
    path('add_location/', views.location_view.add_location, name="add_location"),
    path('update_location/<str:pk>/', views.location_view.update_location, name="update_location"),
    path('delete_location/<str:pk>/', views.location_view.delete_location, name="delete_location"),
    path('filter_location/', views.location_view.filter_location, name="filter_location"),

    # Weekend
    path('weekends/', views.weekend_view.weekends, name="weekends"),
    path('add_weekend/', views.weekend_view.add_weekend, name="add_weekend"),
    path('update_weekend/<str:pk>/', views.weekend_view.update_weekend, name="update_weekend"),
    path('delete_weekend/<str:pk>/', views.weekend_view.delete_weekend, name="delete_weekend"),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
