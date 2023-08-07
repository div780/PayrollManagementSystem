from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import EmployeeForm
from .models import Employee, Salary
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter



def aboutUs(request):
    return render(request, "aboutUs.html")


def removeEmployee(request):
    employee=Employee.objects.all()
    salary=Salary.objects.all()
    context = {
        'employees': employee,
        'salary': salary
    }
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        empl = get_object_or_404(Employee, employee_id=employee_id)
        sal=get_object_or_404(Salary,employee_id=employee_id)
        empl.delete()
        sal.delete()
        return render(request,"localAdmin.html")
    
    return render(request,"removeEmployee.html",context)

def ViewSalaryDetails(request):
    salary=Salary.objects.all()
    return render(request,"viewSalary.html",{'salary':salary})


def salaryDetails(request):
    employees = Employee.objects.all()
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        
        basic_salary = request.POST['basic_salary']
        allowances = request.POST.get('allowances', 0)
        tax = request.POST.get('tax', 0)
        insurance = request.POST.get('insurance', 0)
        otherDeductions = request.POST.get('otherDeductions', 0)
        overtime_pay = request.POST.get('overtime_pay', 0)
        bonuses = request.POST.get('bonuses', 0)
        
        # Calculate net salary
        net_salary = float(basic_salary) + float(allowances) - float(otherDeductions) + float(overtime_pay) + float(bonuses)- float(tax)- float(insurance)
        
        # Save the data to the database
        salary = Salary.objects.create(
            employee_id=employee_id,
            basic_salary=basic_salary,
            allowances=allowances,
            tax=tax,
            insurance=insurance,
            otherDeductions=otherDeductions,
            overtime_pay=overtime_pay,
            bonuses=bonuses,
            net_salary=net_salary
        )
        
        # Redirect to a success page or display a success message
        return render(request,"localAdmin.html")
    
    return render(request,"salaryDetails.html",{'employees': employees})

def generate_payslip_pdf(employee, salary):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{employee.employee_id}.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Set font styles
    p.setFont("Helvetica-Bold", 14)
    p.setFont("Helvetica", 12)

    # Add payslip details
    p.drawString(100, 750, "Payslip")
    p.drawString(100, 700, "Employee Name: {}".format(employee.first_name + " " + employee.last_name))
    p.drawString(100, 675, "Employee ID: {}".format(employee.employee_id))
    p.drawString(100, 650, "Month: May")  # Hard-coded month as "May"
    p.drawString(100, 625, "Year: 2023")  # Hard-coded year as "2023"

    # Add salary details
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 575, "Earnings")
    p.setFont("Helvetica", 12)
    p.drawString(200, 550, "Basic Salary: ${:.2f}".format(salary.basic_salary))
    p.drawString(200, 525, "Allowances: ${:.2f}".format(salary.allowances))
    p.drawString(200, 500, "Bonus: ${:.2f}".format(salary.bonuses))
    p.drawString(100, 450, "Deductions")
    p.drawString(200, 425, "Tax: ${:.2f}".format(salary.tax))
    p.drawString(200, 400, "Insurance: ${:.2f}".format(salary.insurance))
    p.drawString(200, 375, "Other Deductions: ${:.2f}".format(salary.otherDeductions))

    # Add total earnings and deductions
    total_earnings = salary.basic_salary + salary.allowances + salary.bonuses
    total_deductions = salary.tax + salary.insurance + salary.otherDeductions
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 325, "Total Earnings: {:.2f}".format(total_earnings))
    p.drawString(100, 300, "Total Deductions: {:.2f}".format(total_deductions))

    # Add net salary
    net_salary = total_earnings - total_deductions
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 250, "Net Salary: {:.2f}".format(net_salary))
    # Save the PDF
    p.showPage()
    p.save()

    return response



def payslip(request, employee_id):
    try:
        employee = Employee.objects.get(employee_id=employee_id)
        salary = Salary.objects.get(employee_id=employee_id)
        return generate_payslip_pdf(employee, salary)
    except (Employee.DoesNotExist, Salary.DoesNotExist):
        return HttpResponse('Employee or salary not found.')

# Create your views here.
def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    

    if request.method == 'POST':
        # Retrieve the updated attributes from the form
        new_email = request.POST.get('email')
        new_phone = request.POST.get('phone')
        new_address = request.POST.get('address')
        new_pincode = request.POST.get('pincode')

        # Modify the attributes of the retrieved employee object
        employee.email = new_email
        employee.mobile_number = new_phone
        employee.address=new_address
        employee.pincode=new_pincode

        # Save the updated employee object back to the database
        employee.save()

        # Redirect to a success page or perform any other actions
        return render(request, 'employee.html',{'employee': employee})

    # Render the update form with the existing employee's attributes
    return render(request, 'updateEmployee.html', {'employee': employee})

def employee_list(request):
    employees = Employee.objects.all()  # Retrieve all employees from the database
    return render(request, 'employee_list.html', {'employees': employees})


def home(request):
    return render(request,"home.html")



def success(request):
    return render(request, 'EmployeeDetailsSuccess.html')


def employee_details(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('/success')  # Redirect to a success page
    else:
        form = EmployeeForm()
    return render(request, 'employeeForm.html', {'form': form})

def employeePage(request):
    return render(request,"employee.html")

def employeeLogin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        try:
            employee = Employee.objects.get(employee_id=username)
            
            salary=Salary.objects.get(employee_id=username)
            context = {
                'employee': employee,
                'salary': salary
            }
            if str(employee.employee_id)==password:
                return render(request, 'employee.html', context)
            else:
                return render(request,"incorrectCredentials.html")

            
        except ObjectDoesNotExist:
            return render(request,"incorrectCredentials.html")
    else:
        return render(request,"employeeLogin.html")
    


def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/localAdmin')
        else:
            return redirect('/signin')
    else:
        return render(request,"login.html")
        
        
def signout(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')

        try:
            user = User.objects.get(username=username)
            messages.error(request, "Username is already taken.")
            return redirect('/signup')
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Sign up successful!")
            return redirect('/signin')

    return render(request, 'signup.html')

def localAdmin(request):
    return render(request,'localAdmin.html')
    
    
