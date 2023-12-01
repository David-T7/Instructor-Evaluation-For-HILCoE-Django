import json
from django.shortcuts import render
from Account.forms import CustomUserCreationForm
from Account.models import StudentInfo , Account
from Evaluation.models import Criteria, CriteriaSection, EvaluationCriteria
from Instructor.models import Instructor
from Staff.models import StaffEvaluationResult
from .forms import EvaluationSearchForm, StudentCreationForm
from django.contrib import  messages
from django.shortcuts import redirect, render
from .models import Student , StudentCourseEnrollment, StudentEvaluationResult
from Course.models import Course , Term , CourseInstructor
from django.db.models import Avg
from django.db.models import F, Func, Value
from django.db.models.functions import Cast
from django.db import models
from django.db.models import Q



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
    term  = Term.objects.get(EvaluationDone = False)
    courseinstructors = []    
    # Create dictionaries to store course and instructor data
    courseData = {}
    instructorData = {}

    # Populate course and instructor data based on student enrollments
    for enrollment in student_enrollments:
        course = enrollment.course
        course_instructors = CourseInstructor.objects.filter(Course = course ,Batch = student.Batch )
        courseinstructors.append(course_instructors)
        for courseinstructor in course_instructors:        
            courseData[courseinstructor.Instructors.Instructor_id] = {
                'coursename': courseinstructor.Course.CourseName,
                'creditHours': courseinstructor.Course.CreditHour,
                'courseId': courseinstructor.Course.Course_id,
                'courseType':courseinstructor.CourseType,
            }

            instructorData[courseinstructor.Instructors.Instructor_id] = [
            {'FirstName': courseinstructor.Instructors.FirstName, 'LastName': courseinstructor.Instructors.LastName , 'profilePic':'/static/'+str(courseinstructor.Instructors.ProfilePic) }
            ]
    for course in courseinstructors:
         print("course instructor to be send is ", course)
         
    context = {
        'active_page': 'home',
        'studentenrollements': student_enrollments,
        'courseData': json.dumps(courseData),
        'instructorData': json.dumps(instructorData),
        'courseinstructors':courseinstructors,
        'term':term,
    }

    print("coursedata" , courseData  , "instructordata", instructorData)
    return render(request, 'student/studenthome.html', context)

def student_evaluate_page(request):
    term = Term.objects.last()
    student = Student.objects.get(Account_id=request.user)
    student_enrollments = StudentCourseEnrollment.objects.filter(student=student, term=term)
    student_evaluation_result = StudentEvaluationResult.objects.filter(Student_id = student)
    evaluated_courses_types = []
    evaluated_instructors = []
    course_instructors = []    
    if student_evaluation_result:
        for student_evaluation in student_evaluation_result:
            evaluated_instructors.append(student_evaluation.Instructor_id.Instructor_id)
            evaluated_courses_types.append(student_evaluation.CourseType)
    courses_data = []
    for enrollment in student_enrollments:
        instructors_data = []
        for courseinstructors in CourseInstructor.objects.filter(Course = enrollment.course ):
            course_instructors.append(courseinstructors)
            instructor_info = {
                'name': f'{courseinstructors.Instructors.FirstName} {courseinstructors.Instructors.LastName}',
                'title': courseinstructors.Instructors.Title,
                'instructor_id':courseinstructors.Instructors.Instructor_id , 
                'profile_pic': courseinstructors.Instructors.ProfilePic.url if courseinstructors.Instructors.ProfilePic else None,
            }
            instructors_data.append(instructor_info)

        course_data = {
            'course_name': enrollment.course.CourseName,
            'course_id':enrollment.course.Course_id,
            'instructors': instructors_data,
            'evaluate_url': f'/evaluate/{enrollment.id}/',  # Replace with the actual URL for evaluation
        }
        courses_data.append(course_data)

    context = {
        'courses_data': courses_data,
        'term': term,
        'active_page':'evaluation',
        'student':student,
        'evaluated_courses_types':evaluated_courses_types,
        'course_instructors':course_instructors,
        'evaluated_instructors':evaluated_instructors,
    }

    return render(request, 'student/evaluate.html', context)
    
def evaluate_course(request, student_id, course_id, instructor_id , course_type):
    evaluationMapping= {'Excellent':5,'Very Good':4,'Good':3,'Poor':2,'Very Poor':1}
    evaluated_criteria_descriptions = set()
    student = Student.objects.get(Student_id=student_id)
    course = Course.objects.get(Course_id=course_id)
    instructor = Instructor.objects.get(Instructor_id=instructor_id)

    # Find the latest term where evaluation is not done
    term = Term.objects.filter(Courses_Given=course, EvaluationDone=False).order_by('-Year', 'Season').first()

    if not term:
        messages.warning(request, 'Course evaluation is already completed for all terms.')
        return redirect('evaluate')  # Redirect to home or another page

    enrollment = StudentCourseEnrollment.objects.get(student=student, course=course, term=term)
    all_criteria_objects = EvaluationCriteria.objects.get(Evaluator='Student' , Evaluatee = course_type)  # Adjust based on your criteria
    # all_criteria_objects = EvaluationCriteria.objects.all()
    # Collect all distinct criteria sections using Python
    all_criteria_data = all_criteria_objects.Criteria_data.all()
    # print("all criteria data " , all_criteria_data)
    all_criteria = []
    criteria_sections = []
    desired_order = ['Course Organization', 'Knowledge of the subject matter', 'Teaching Methods',
                    'Student Involvement', 'Evaluation Methods' , 'Personality Traits' , 'Availability and Support']
    for criteria_object in all_criteria_data:
        criteria = Criteria.objects.get(Criteria_id= criteria_object.Criteria_id) 
        if criteria.Section not in  criteria_sections :
            all_criteria.append(criteria)
            criteria_sections.append(criteria.Section)
        # print("criteria section" , criteria.Section )
    print("all criteria data are ", all_criteria)
    # print("all criteria sections before sort: ", criteria_sections)
    criteria_sections.sort(key=lambda x: desired_order.index(x.Section))
    print("after sort criteria sections: ", criteria_sections)
   
        
    criteria_results = {}
    error_occured = False
    if request.method == 'POST':
        submitted_data = request.POST.copy()
        for key, value in submitted_data.items():
                if key.startswith('criteria_'):
                    criteria_id = key.replace('criteria_', '')
                    criteria_results[criteria_id] = value
        evaluation_result = {}
        for criteria in all_criteria_data:
            score = request.POST.get(f'criteria_{criteria.Criteria_id}')
            if score:
                section_name = criteria.Section.Section
                if section_name not in evaluation_result:
                        evaluation_result[section_name] = {}
                evaluation_result[section_name][str(criteria.description)] = evaluationMapping[score]
                evaluated_criteria_descriptions.add(criteria.description)
        # Get all unique criteria descriptions
        all_criteria_descriptions = set(criteria.description for criteria in all_criteria_data)        
        # print("evaluation resullt",evaluation_result)     
        if evaluation_result and evaluated_criteria_descriptions == all_criteria_descriptions:
            result_instance, created = StudentEvaluationResult.objects.get_or_create(
                Student_id=student,
                Course_id=course,
                Instructor_id=instructor,
                CourseType= course_type , 
                Term_id=term,
                defaults={'EvaluationResult': evaluation_result, 'EvaluationDone': True}
            )

            if not created:
                messages.error(request, 'Please evaluate all criteria descriptions before submitting!' )
                error_occured = True
            else:
                messages.success(request, 'You have completed Evaluation for course '+ course.CourseName) 
                return redirect('evaluate')  # Redirect to home or another page after evaluation
        else:
            messages.error(request, 'Please evaluate all criteria descriptions before submitting!')
            error_occured = True

    
    context = {
        'enrollment': enrollment,
        'criteria_data': all_criteria_data,
        'student':student, 
        'active_page':'evaluation',
        'all_criteria_sections': all_criteria ,
        'criteria_sections':criteria_sections,
        'instructor':instructor,
        'course_type':course_type,
        'criteria_results' : criteria_results,
        'error_occured': error_occured,
        
    }
    print('criteria result is ', criteria_results )
    return render(request, 'student/evaluate_course.html', context)
    
def student_evaluation_reports(request , evaluator):
    # Retrieve all unique instructors evaluated by students for the term
    courses = Course.objects.all()

    # Prepare a list to store instructor information with average scores
    instructor_data = []
    
    # Iterate through instructors and calculate average scores
    for course_type in ['Lecture', 'Lab']:
        for course in courses:
            total_avg_score = 0
            instructor = None
            evaluations = None
            if evaluator == 'student':
                evaluations = StudentEvaluationResult.objects.filter(
                    Course_id =course,
                    Term_id=Term.objects.last(),
                    EvaluationDone=True ,
                    CourseType = course_type
                    )
            elif evaluator == 'staff':
                evaluations = StaffEvaluationResult.objects.filter(
                    Course_id =course,
                    Term_id=Term.objects.last(),
                    EvaluationDone=True ,
                    CourseType = course_type
                    )
            
            if evaluations:
                current_evaluator = None
                for evaluation in evaluations:
                    if not current_evaluator:
                        if StudentEvaluationResult.objects.filter(Result_id =evaluation.Result_id):current_evaluator='student'
                        else: current_evaluator='staff' 
                    if not instructor:
                        instructor = evaluation.Instructor_id
                    avg_score = 0
                    len = 0
                    # Extract values from the EvaluationResult JSON field
                    for category, sub_dict in evaluation.EvaluationResult.items():
                        for criterion, score in sub_dict.items():
                            if isinstance(score, (int, float)):
                                len+=1
                                avg_score += score
                    avg_score/= len
                    total_avg_score += avg_score
                    print("average score is " , avg_score)
                    # Append instructor information to the list
                if evaluations: total_avg_score /=  evaluations.__len__()
                instructor_data.append({
                    'instructor': instructor,
                    'course': course,
                    'course_type': course_type,
                    'average_score': total_avg_score.__round__(2),
                    'current_evaluator':current_evaluator,
                    })
            

    context = {'instructor_data': instructor_data , 'active_page':'report', 'evaluator':evaluator}
    print("instructor infor ",instructor_data)
    return render(request, 'academichead/evaluation_reports.html', context)    
    
def moreStudentEvaluationDetails(request , instructor_id , course_id , course_type , evaluator):
    instructor = Instructor.objects.get(Instructor_id = instructor_id)
    course = Course.objects.get(Course_id  = course_id)
    evaluation = None
    if evaluator == 'student':
        evaluations = StudentEvaluationResult.objects.filter(
                Course_id =course,
                Term_id=Term.objects.last(),
                EvaluationDone=True ,
                CourseType = course_type,
                Instructor_id = instructor
                    )
    elif evaluator == 'staff':
            evaluations = StaffEvaluationResult.objects.filter(
                Course_id =course,
                Term_id=Term.objects.last(),
                EvaluationDone=True ,
                CourseType = course_type,
                Instructor_id = instructor
                    )
    criteria_average_details = []
    criteria = []
    criteria_category = {}
    criteria_sections = []
    criteria_average_Scores = []
    for evaluation in evaluations:
        for category, sub_dict in evaluation.EvaluationResult.items():
            if category not in criteria_sections:criteria_sections.append(category)
            average_score = 0
            for criterion, score in sub_dict.items():
                if criterion not in criteria:
                    criteria_category[criterion] = category
                criteria.append(criterion)
                criteria_average_details.append({
                    'category': category,
                    'criteria': criterion,
                    'score': score,
                    })
    print ("criteria dic is " , criteria_category)
    for  criteria , category in criteria_category.items():
        average_score = 0
        len = 0
        for average_details in criteria_average_details:
            if average_details['category'] == category and average_details['criteria'] == criteria:
                average_score += average_details['score']
                len+=1
        criteria_average_Scores.append(
            {
                'category': category,
                'criteria': criteria,
                'score': average_score / len,  
            }
        )
        
    print ('criteria_average_Scores is ' , criteria_average_Scores)               
    context = {'criteria_average_Scores':criteria_average_Scores  , 
               'criteria_sections':criteria_sections , 
               'instructor':instructor ,
               'evaluation':evaluation, 
               'active_page':'report',
               'evaluator':evaluator , 
               }
    return render(request, 'academichead/moreevaluationdetials.html', context)    

def search_evaluation(request):
    if request.method == 'POST':
        print("in post before evaluting form")
        form = EvaluationSearchForm(request.POST)
        evaluation_result_list = []
        instructor_data = []
        if form.is_valid():
            query_params = {}
            if form.cleaned_data['evaluator']:
                evaluator = form.cleaned_data['evaluator']
            else:
                evaluator = 'both'
            # Check each form field and add it to the query_params if it's not empty
            for field_name, value in form.cleaned_data.items():
                if value and field_name!= 'evaluator':
                    query_params[f"{field_name}"] = value
            
            # Perform your search based on the dynamic query_params
            print('query parameters ',query_params)
            evaluation_result_list.clear()
            if evaluator == 'Student':
                result = StudentEvaluationResult.objects.filter(Q(**query_params))
                if result:
                    evaluation_result_list.append(result)
            elif evaluator == 'Staff':
                result = StaffEvaluationResult.objects.filter(Q(**query_params))
                if(result):
                    evaluation_result_list.append(result)
            else:
                result1 = StudentEvaluationResult.objects.filter(Q(**query_params))
                result2 = StaffEvaluationResult.objects.filter(Q(**query_params))
                if result1:evaluation_result_list.append(result1)
                if result2:evaluation_result_list.append(result2)
            if evaluation_result_list.__len__() > 0:
                for evaluations in evaluation_result_list:
                    instructor = None
                    course = None
                    course_type = None
                    total_avg_score = 0
                    current_evaluator = None
                    for evaluation in evaluations:
                        if not current_evaluator:
                            if StudentEvaluationResult.objects.filter(Result_id =evaluation.Result_id):current_evaluator='student'
                            else: current_evaluator='staff' 
                        instructor = evaluation.Instructor_id
                        course = evaluation.Course_id
                        course_type = evaluation.CourseType
                        avg_score = 0
                        len = 0
                        # Extract values from the EvaluationResult JSON field
                        for category, sub_dict in evaluation.EvaluationResult.items():
                            for criterion, score in sub_dict.items():
                                if isinstance(score, (int, float)):
                                    len+=1
                                    avg_score += score
                        avg_score/= len
                        total_avg_score += avg_score
                        print("average score is " , avg_score)
                        # Append instructor information to the list
                    if evaluations: total_avg_score /=  evaluations.__len__()
                    print('current evaluator' ,current_evaluator)
                    instructor_data.append({
                        'instructor': instructor,
                        'course': course,
                        'course_type': course_type,
                        'average_score': total_avg_score.__round__(2),
                        'current_evaluator':current_evaluator
                        })
            else:
                print("evaluation list not found")
                messages.error(request, 'No result found!')
                return redirect('search_evaluation')

                
            context = {'instructor_data': instructor_data , 'active_page':'report', 'evaluator':evaluator}
        print("instructor infor ",instructor_data)
        return render(request, 'academichead/evaluation_reports.html', context)

    else:
        form = EvaluationSearchForm()
        print("in get")
        return render(request, 'academichead/evaluation_search.html', {'form': form , 'active_page':'report',})            
    

