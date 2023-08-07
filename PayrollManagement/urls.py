"""
URL configuration for PayrollManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PayrollApp.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home),
    path('',home),
    path('signin/',signin),
    path('signout/',signout),
    path('signup/',register),
    path('localAdmin/',localAdmin),
    path('viewSalaryDetails/',ViewSalaryDetails),
    path('employeeDetails/', employee_details,name='employee_details'),
    path('success/',success),
    path('employeeList/', employee_list),
    path('employeeLogin/', employeeLogin),
    path('employeePage/', employeePage),
    path('removeEmployee/', removeEmployee),
    path('updateEmployee/<employee_id>/', update_employee),
    path('salaryDetails/',salaryDetails),
    path('payslip/<employee_id>/', payslip),
    path('aboutUs/',aboutUs),

]


