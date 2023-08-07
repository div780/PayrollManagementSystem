# models.py

from django.db import models

class Employee(models.Model):
    class Meta:
        app_label = 'PayrollApp'
    employee_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    start_date = models.DateField()


class Salary(models.Model):
    employee_id = models.CharField(max_length=100)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    insurance = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    otherDeductions = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
