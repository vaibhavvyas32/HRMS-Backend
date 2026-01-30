from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeListPagination(PageNumberPagination):
    """Pagination for employee list (PRD §9: recommended for scaling)."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class EmployeeListCreateView(ListCreateAPIView):
    """
    GET: List all employees (ordered by created_at). Paginated.
    POST: Create a new employee. Returns 201 with created object on success.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = EmployeeListPagination

    def get_queryset(self):
        return Employee.objects.all().order_by('created_at')


class EmployeeDestroyView(DestroyAPIView):
    """
    DELETE: Permanently delete an employee. Associated attendance records
    are removed via CASCADE. Returns 204 No Content on success, 404 if not found.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
