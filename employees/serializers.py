from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """Validates and serializes Employee. employee_id is read-only on update."""

    class Meta:
        model = Employee
        fields = [
            'id',
            'employee_id',
            'full_name',
            'email',
            'department',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['employee_id'].read_only = True

    def validate_employee_id(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Employee ID is required and cannot be blank.')
        value = value.strip()
        qs = Employee.objects.filter(employee_id=value)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                'An employee with this employee ID already exists.'
            )
        return value

    def validate_full_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Full name is required and cannot be blank.')
        return value.strip()

    def validate_email(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Email is required and cannot be blank.')
        value = value.strip().lower()
        qs = Employee.objects.filter(email__iexact=value)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                'An employee with this email already exists.'
            )
        return value

    def validate_department(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Department is required and cannot be blank.')
        return value.strip()
