from django.shortcuts import render
from Account.forms import CustomUserCreationForm
from Account.models import StudentInfo , Account
from .forms import StudentCreationForm
from django.contrib import  messages
from django.shortcuts import redirect, render
from .models import Student , StudentCourseEnrollment
from Course.models import Course
# Create your views here.

def Register(request):
    form1 = StudentCreationForm()   # using the donor creation form created in forms.py
    form2= CustomUserCreationForm()
    studentinfo = None
    if request.method == 'POST':
        form1= StudentCreationForm(request.POST)  # getting values send from the page
        form2 = CustomUserCreationForm(request.POST)
        if (form1.is_valid() and form2.is_valid()):  # checking  values send from the page are valid  
            try:
                student_id = request.POST['Student_id']
                try:
                    studentinfo = StudentInfo.objects.get(Student_id=student_id)
                    print("student id found")
                    if(studentinfo.Registered==False):
                        print("creating account....")
                        account = form2.save(commit=False) # saving the values but not in the table
                        account.Role='Student'
                        account.email = request.POST['email']
                        account.save() # saving the user account
                        print("user accoutn created")
                        student = form1.save(commit=False)
                        student.Account_id = account
                        student.Batch = studentinfo.Batch
                        student.Department = studentinfo.Department
                        student.save()
                        studentinfo.Registered = True
                        messages.success(request, 'Successfully Registered')
                        return redirect('/login/Donor')
                    elif (studentinfo.Registered==True):
                        messages.success(request, 'A user with the id already exists')
                        print("A user with the id already exists")
                except:
                    if(studentinfo == None):
                        messages.success(request, 'Please enter a valid id')
                        
            except:
                print("exception catched")
        else:
            print("invalid form")
    context = {'form1': form1,'form2':form2, 'sender':'student'}  # forms that are passed to the page rendered
    return render(request, 'registerpage.html',context)

def Studnets(request):
    context = {'user':request.user}
    return render(request , 'student/student.html' , context)

def studenthomepage(request):
    student = Student.objects.get(Account_id = request.user)
    student_enrollments = StudentCourseEnrollment.objects.filter(student = student)
    context = {'active_page':'home' , 'studentenrollements':student_enrollments , }
    return render(request , 'student/studenthome.html',context)