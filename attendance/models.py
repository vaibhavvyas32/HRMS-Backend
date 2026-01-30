from django.db import models

from employees.models import Employee


class Attendance(models.Model):
    """Single attendance entry per employee per date. Status is present or absent."""

    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=10, choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'date'],
                name='unique_employee_date',
            ),
        ]
        ordering = ['-date', 'employee']

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"
