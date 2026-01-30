from django.urls import path

from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.EmployeeListCreateView.as_view(), name='list-create'),
    path('<int:pk>/', views.EmployeeDestroyView.as_view(), name='destroy'),
]
