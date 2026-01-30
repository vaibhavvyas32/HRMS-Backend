from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from employees.models import Employee

from .models import Attendance
from .serializers import AttendanceListSerializer, AttendanceSerializer


class AttendanceCreateView(CreateAPIView):
    """
    POST: Mark attendance for an employee on a date.
    Returns 201 with created record on success.
    Returns 404 if employee does not exist; 400 for validation errors.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):
        employee_pk = request.data.get('employee')
        if employee_pk is not None:
            if not Employee.objects.filter(pk=employee_pk).exists():
                return Response(
                    {'message': 'Employee not found.', 'errors': {}},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return super().create(request, *args, **kwargs)


class EmployeeAttendanceListView(ListAPIView):
    """
    GET: List attendance records for an employee (by employee_id string).
    Ordered by date descending. Returns 404 if employee not found.
    Response includes date, status, and basic employee information (PRD §8).
    """
    serializer_class = AttendanceListSerializer

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        employee = Employee.objects.filter(employee_id=employee_id).first()
        if employee is None:
            return Attendance.objects.none()
        return Attendance.objects.filter(employee=employee).order_by('-date')

    def list(self, request, *args, **kwargs):
        employee_id = self.kwargs['employee_id']
        if not Employee.objects.filter(employee_id=employee_id).exists():
            return Response(
                {'message': 'Employee not found.', 'errors': {}},
                status=status.HTTP_404_NOT_FOUND,
            )
        return super().list(request, *args, **kwargs)
