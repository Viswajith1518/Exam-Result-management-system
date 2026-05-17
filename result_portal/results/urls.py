from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/students/', views.student_list, name='student_list'),
    path('admin-panel/students/add/', views.add_student, name='add_student'),
    path('admin-panel/students/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('admin-panel/results/', views.manage_results, name='manage_results'),
    path('admin-panel/results/add/', views.add_result, name='add_result'),
    path('admin-panel/results/delete/<int:pk>/', views.delete_result, name='delete_result'),

    path('dashboard/', views.student_dashboard, name='student_dashboard'),
]