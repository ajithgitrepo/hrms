from django.urls import path, re_path, include
from app import views 
from app.views.restriction_view import admin_only,role_name

urlpatterns = [
   
    #Home page
    path('', views.dashborad_view.index, name='home'),
	path('home/', views.dashborad_view.index, name='home'),
  
    #Self Service
    path('profile/', views.self_service_view.profile, name="profile"),
    path('change_password/', views.self_service_view.change_password, name='change_password'),
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
    path('self_vaccination_details/', views.self_service_view.self_vaccination_details, name="self_vaccination_details"),

    # Employee 
	path('employees/', views.employee_view.employees, name="employees"),
	path('add_employee/', views.employee_view.add_employee, name="add_employee"),
    path('import_employee/', views.employee_view.import_employee, name="import_employee"),
	path('update_employee/<str:pk>/', views.employee_view.update_employee, name="update_employee"),
	path('update_employee_emp/<str:pk>/', views.employee_view.update_employee_emp, name="update_employee_emp"),
	path('delete_employee/<str:pk>/', views.employee_view.delete_employee, name="delete_employee"),
	path('status_employee/<str:pk>/<str:val>/', views.employee_view.status_employee, name="status_employee"),
	path('snippets', views.employee_view.snippets, name="snippets"),
	path('reporting/', views.employee_view.reporting, name="reporting"),
	path('filter_employee', views.employee_view.filter_employee, name="filter_employee"),
    path('view_more', views.employee_view.view_more, name="view_more"),
    
    
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

    # Business_unit 
    path('business_units/', views.business_unit_view.business_units, name="business_units"),
    path('add_business_unit/', views.business_unit_view.add_business_unit, name="add_business_unit"),
    path('delete_business_unit/<str:pk>/', views.business_unit_view.delete_business_unit, name="delete_business_unit"),

    # Variable Salary 
    path('variable_salaries/', views.variable_salary_view.variable_salaries, name="variable_salaries"),
    path('add_variable_salary/', views.variable_salary_view.add_variable_salary, name="add_variable_salary"),
    path('delete_variable_salary/<str:pk>/', views.variable_salary_view.delete_variable_salary, name="delete_variable_salary"),

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
    # path('edit_comp_off/<str:pk>/', admin_only(views.leave_type_view.edit_comp_off), name="edit_comp_off"),
   
   
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
    path('status_onboard_employees/<str:pk>/<str:val>/', views.onboard_employee_view.status_onboard_employees, name="status_onboard_employees"),
    path('filter_onboard_employees/<str:status>/', views.onboard_employee_view.filter_onboard_employees, name="filter_onboard_employees"),
    path('enroll_info/', views.onboard_employee_view.enroll_info, name="enroll_info"),
    path('approve/', views.onboard_employee_view.approve, name="approve"),
    path('business_approve/', views.onboard_employee_view.business_approve, name="business_approve"),
    path('approve_status/', views.onboard_employee_view.approve_status, name="approve_status"),
    path('update_enroll_info/', views.onboard_employee_view.update_enroll_info, name="update_enroll_info"),
    path('update_enroll/', views.onboard_employee_view.update_enroll, name="update_enroll"),
    path('enroll_more_info/', views.onboard_employee_view.enroll_more_info, name="enroll_more_info"),
    path('view_more/', views.onboard_employee_view.view_more, name="view_more"),
    path('get_business_unit/', views.onboard_employee_view.get_business_unit, name="get_business_unit"),
    path('get_variable_salary/', views.onboard_employee_view.get_variable_salary, name="get_variable_salary"),







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
    path('attn_more_info/', views.attendance_view.attn_more_info, name='attn_more_info'),

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
   	path('travel_expense_approve/', views.travel_expense_view.travel_expense_approve, name="travel_expense_approve"),

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
    path('assets_approve/', views.asset_deatails_view.assets_approve, name="assets_approve"),
    
    # Holiday Details
    path('holiday_details/', views.holiday_details_view.holiday_details, name="holiday_details"),
    path('add_holiday_details', views.holiday_details_view.add_holiday_details, name="add_holiday_details"),
    path('delete_holiday_details/<str:pk>/', views.holiday_details_view.delete_holiday_details, name="delete_holiday_details"),
    path('filter_holiday/', views.holiday_details_view.filter_holiday, name="filter_holiday"),
    path('edit_holiday_details/<str:pk>/', views.holiday_details_view.edit_holiday_details, name="edit_holiday_details"),

    # Exit Details
    path('exit_details/', views.exit_deatails_view.exit_details, name="exit_details"),
    path('add_exit_details', views.exit_deatails_view.add_exit_details, name="add_exit_details"),
    path('delete_employee_exit_details/<str:pk>/', views.exit_deatails_view.delete_employee_exit_details, name="delete_employee_exit_details"),
    path('snippets_exit_employee_all_info', views.snippets_exit_employee_all_info, name="snippets_exit_employee_all_info"),
    path('status_exit_employees/<str:pk>/<str:val>/', views.exit_deatails_view.status_exit_employees, name="status_exit_employees"),

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

	# Work From Home
    path('workhome_requests/', views.workhome_view.workhome_requests, name="workhome_requests"),
    path('add_workhome_request/', views.workhome_view.add_workhome_request, name="add_workhome_request"),
    path('delete_workhome/<str:pk>/', views.workhome_view.delete_workhome, name="delete_workhome"),
    # Work From Home Approve
    path('workhome_approves/', views.workhome_approve_view.workhome_approves, name="workhome_approves"),
    path('change_wfh_status/', views.workhome_approve_view.change_wfh_status, name="change_wfh_status"),

    #Vaccination Details 
    path('vaccination_details/', views.vaccination_details_view.vaccination_details, name="vaccination_details"),
    path('add_vaccination_details', views.vaccination_details_view.add_vaccination_details, name="add_vaccination_details"),
    path('delete_vaccine_details/<str:pk>/', views.vaccination_details_view.delete_vaccine_details, name="delete_vaccine_details"),
    path('snippets_vaccinae_employee_all_info', views.vaccination_details_view.snippets_vaccinae_employee_all_info, name="snippets_vaccinae_employee_all_info"),
    path('filter_vacciate_employees/<str:status>/', views.vaccination_details_view.filter_vacciate_employees, name="filter_vacciate_employees"),
    path('update_vaccination_details/<str:pk>/', views.vaccination_details_view.update_vaccination_details, name="update_vaccination_details"),
    
     # customer_policy 
      path('customer_policy/', views.customer_policy_view.customer_policy, name="customer_policy"),
      path('get_custom_leave_type', views.customer_policy_view.get_custom_leave_type, name="get_custom_leave_type"),
      path('add_custom_leave_type', views.customer_policy_view.add_custom_leave_type, name="add_custom_leave_type"),
      path('get_custom_leave_type_bychange', views.customer_policy_view.get_custom_leave_type_bychange, name="get_custom_leave_type_bychange"),

	
    # client
    path('clients/', views.client_view.clients, name="clients"),
    path('add_client/', views.client_view.add_client, name="add_client"),
    path('delete_client/<str:pk>/', views.client_view.delete_client, name="delete_client"),
    path('info', views.client_view.info, name="info"),
    path('update_client/<str:pk>/', views.client_view.update_client, name="update_client"),

    # Project
    path('projects/', views.project_view.projects, name="projects"),
    path('add_project/', views.project_view.add_project, name="add_project"),
    path('delete_project/<str:pk>/', views.project_view.delete_project, name="delete_project"),
    path('update_project/<str:pk>/', views.project_view.update_project, name="update_project"),

    #Timelogs
    path('timelogs/', views.timelogs_view.timelogs, name="timelogs"),
    path('timelog_checkin/', views.timelogs_view.timelog_checkin, name="timelog_checkin"),
    path('timelog_checkout/', views.timelogs_view.timelog_checkout, name="timelog_checkout"),
    path('filter_timelog/<str:month>/', views.timelogs_view.filter_timelog, name="filter_timelog"),
    path('click_timelog_dahsboard/', views.timelogs_view.click_timelog_dahsboard, name="click_timelog_dahsboard"),

    path('time_logs/', views.timelogs_view.time_logs, name="time_logs"),
    path('time_logs/', views.timelogs_view.time_logs, name="time_logs"),
    path('search_timelog/<str:pk>/<str:month>/', views.timelogs_view.search_timelog, name="search_timelog"),

    # Manual Checkin Request
    path('manual_checkin_details/', views.manual_checkin_view.manual_checkin_details, name="manual_checkin_details"),
    path('add_manual_checkin_details/', views.manual_checkin_view.add_manual_checkin_details, name="add_manual_checkin_details"),
    path('delete_manual_check_details/<str:pk>/', views.manual_checkin_view.delete_manual_check_details, name="delete_manual_check_details"),

     # Reporting To 
    path('reporting_to/', views.reportingto_view.reporting_to, name="reporting_to"),
    path('add_reporting_to/', views.reportingto_view.add_reporting_to, name="add_reporting_to"),
  #  path('update_department/<str:pk>/', views.department_view.update_department, name="update_department"),
    path('delete_reportingto/<str:pk>/', views.reportingto_view.delete_reportingto, name="delete_reportingto"),
    path('status_reporting_employee/<str:emp_id>/<str:pk>/<str:val>/', views.reportingto_view.status_reporting_employee, name="status_reporting_employee"),
    path('filter_reporting_employees/<str:status>/', views.reportingto_view.filter_reporting_employees, name="filter_reporting_employees"),
    
    # Employee Mapping
    path('add_emp_mapping/', views.emp_mapping_view.add_emp_mapping, name="add_emp_mapping"),
    path('emp_mapping/', views.emp_mapping_view.emp_mapping, name="emp_mapping"),
    path('add_emp_mapping/<str:pk>/', views.emp_mapping_view.add_emp_mapping, name="add_emp_mapping"),
    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
