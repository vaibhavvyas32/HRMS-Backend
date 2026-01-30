from rest_framework import serializers

from employees.models import Employee

from .models import Attendance


class EmployeeBasicSerializer(serializers.ModelSerializer):
    """Minimal employee fields for nested use in attendance list (PRD: basic employee information)."""

    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name']


class AttendanceSerializer(serializers.ModelSerializer):
    """Validates and serializes Attendance. Ensures employee exists and no duplicate per employee/date."""

    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        error_messages={'does_not_exist': 'Employee not found.'},
    )

    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'date', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_date(self, value):
        if value is None:
            raise serializers.ValidationError('Date is required.')
        return value

    def validate_status(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Status is required and cannot be blank.')
        value = value.strip().lower()
        valid = [choice[0] for choice in Attendance.Status.choices]
        if value not in valid:
            raise serializers.ValidationError(
                f'Status must be one of: {", ".join(valid)}.'
            )
        return value

    def validate(self, attrs):
        employee = attrs.get('employee') or (self.instance and self.instance.employee)
        date = attrs.get('date') or (self.instance and self.instance.date)
        if employee is None or date is None:
            return attrs

        qs = Attendance.objects.filter(employee=employee, date=date)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                {'non_field_errors': ['Attendance for this employee and date already exists.']}
            )
        return attrs


class AttendanceListSerializer(serializers.ModelSerializer):
    """Read-only serializer for listing attendance with basic employee info (PRD §8)."""

    employee = EmployeeBasicSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'date', 'status', 'created_at']
