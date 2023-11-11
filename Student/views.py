from django.shortcuts import render
from Account.forms import CustomUserCreationForm
from Account.models import StudentInfo
from .forms import StudentCreationForm
from django.contrib import  messages
from django.shortcuts import redirect, render
# Create your views here.

def Register(request):
    form1 = StudentCreationForm()   # using the donor creation form created in forms.py
    form2= CustomUserCreationForm()
    if request.method == 'POST':
        if (form1.is_valid() and form2.is_valid() and form2.is_valid()):  # checking  values send from the page are valid  
            try:
                student_id =  request.POST['Student_id']
                studentinfo = StudentInfo.objects.get(student_id=student_id)
                if(StudentInfo.objects.filter(student_id=student_id) and studentinfo.Registered==False ):
                    account = form2.save(commit=False) # saving the values but not in the table
                    account.Role='Student'
                    account.email = request.POST['Email']
                    account.save() # saving the user account
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
                else:
                     messages.success(request, 'Please enter a valid id')
            except:
                True
    context = {'form1': form1,'form2':form2, 'sender':'student'}  # forms that are passed to the page rendered
    return render(request, 'registerpage.html',context)

def Studnets(request):
    context = {'user':request.user}
    return render(request , 'student/student.html' , context)