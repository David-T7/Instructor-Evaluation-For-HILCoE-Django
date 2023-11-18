import json
from django.shortcuts import render
from Account.forms import CustomUserCreationForm
from Account.models import StudentInfo , Account
from .forms import StudentCreationForm
from django.contrib import  messages
from django.shortcuts import redirect, render
from .models import Student , StudentCourseEnrollment
from Course.models import Course , Term
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
    student = Student.objects.get(Account_id=request.user)
    student_enrollments = StudentCourseEnrollment.objects.filter(student=student)

    # Create dictionaries to store course and instructor data
    courseData = {}
    instructorData = {}

    # Populate course and instructor data based on student enrollments
    for enrollment in student_enrollments:
        course = enrollment.course
        instructors = course.Instructors.all()

        courseData[course.CourseName] = {
            'coursename': course.CourseName,
            'creditHours': course.CreditHour,
            'courseId': course.Course_id,
        }

        instructorData[course.CourseName] = [
            {'FirstName': instructor.FirstName, 'LastName': instructor.LastName , 'profilePic':'/static/'+str(instructor.ProfilePic) }
            for instructor in instructors
        ]

    context = {
        'active_page': 'home',
        'studentenrollements': student_enrollments,
        'courseData': json.dumps(courseData),
        'instructorData': json.dumps(instructorData),
    }

    print("coursedata" , courseData  , "instructordata", instructorData)
    return render(request, 'student/studenthome.html', context)

def student_evaluate_page(request):
    term = Term.objects.last()
    student = Student.objects.get(Account_id=request.user)
    student_enrollments = StudentCourseEnrollment.objects.filter(student=student, term=term)

    courses_data = []
    for enrollment in student_enrollments:
        instructors_data = []
        for instructor in enrollment.course.Instructors.all():
            instructor_info = {
                'name': f'{instructor.FirstName} {instructor.LastName}',
                'title': instructor.Title,
                'profile_pic': instructor.ProfilePic.url if instructor.ProfilePic else None,
            }
            instructors_data.append(instructor_info)

        course_data = {
            'course_name': enrollment.course.CourseName,
            'instructors': instructors_data,
            'evaluate_url': f'/evaluate/{enrollment.id}/',  # Replace with the actual URL for evaluation
        }
        courses_data.append(course_data)

    context = {
        'courses_data': courses_data,
        'term': term,
        'active_page':'evaluation',
    }

    return render(request, 'student/evaluate.html', context)
    
    
    
    
    
    

