from django.urls import path

from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.AttendanceCreateView.as_view(), name='create'),
    path('employee/<str:employee_id>/', views.EmployeeAttendanceListView.as_view(), name='list-by-employee'),
]
