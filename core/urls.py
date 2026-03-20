from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('faculty/', views.faculty_list, name='faculty_list'),

    path('add-student/', views.add_student, name='add_student'),
    path('student/<int:id>/', views.student_detail, name='student_detail'),

    path('change-password/', views.change_password, name='change_password'),
    path('student/<int:id>/', views.student_detail, name='student_detail'),
    path('student/<int:id>/edit/', views.student_edit, name='student_edit'),

    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/view/<int:id>/', views.faculty_view, name='faculty_view'),
    path('faculty/edit/<int:id>/', views.faculty_edit, name='faculty_edit'),
    path('faculty/add/', views.add_faculty, name='add_faculty'),

    path('export/', views.export_view, name='export'),
    path('export-excel/', views.export_excel, name='export_excel'),
    path('student/full/<int:id>/', views.student_full_details, name='student_full_details'),
    path('logout/', views.logout_view, name='logout'),
    path('students/', views.student_list, name='student_list'),
    
    path('departments/', views.programmes, name='departments'),

    path('student/<int:id>/delete/', views.delete_student, name='delete_student'),
    path('faculty/<int:id>/delete/', views.delete_faculty, name='delete_faculty'),
    path('digilocker/', views.digilocker, name='digilocker'),
]
