from django.shortcuts import redirect, render
from Course.models import Course, CourseInstructor, Term
from Evaluation.models import Criteria, EvaluationCriteria
from Instructor.models import Instructor
from Student.models import StudentCourseEnrollment
from .models import Staff, StaffEvaluationResult
from django.contrib import  messages
# Create your views here.
def stafflandingpage(request): 
    return render(request , 'stafflandingpage.html')
def staffHomePage(request):
    context = { 'active_page': 'home',}
    return render(request , 'staff/staffhome.html' , context)

def staff_evaluate_page(request):
    term = Term.objects.last()
    staff = Staff.objects.get(Account_id=request.user)
    student_enrollments = StudentCourseEnrollment.objects.filter(term=term)
    staff_evaluation_result = StaffEvaluationResult.objects.filter(Staff_id = staff)
    evaluated_courses_types = []
    evaluated_instructors = []
    course_instructors = []    
    if staff_evaluation_result:
        for staff_evaluation in staff_evaluation_result:
            evaluated_instructors.append(staff_evaluation.Instructor_id.Instructor_id)
            evaluated_courses_types.append(staff_evaluation.CourseType)
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
        'staff':staff,
        'evaluated_courses_types':evaluated_courses_types,
        'course_instructors':course_instructors,
        'evaluated_instructors':evaluated_instructors,
    }

    return render(request, 'staff/evaluate.html', context)

def staff_evaluate_course(request, staff_id, course_id, instructor_id  , course_type):
    evaluationMapping= {'Excellent':5,'Very Good':4,'Good':3,'Poor':2,'Very Poor':1}
    evaluated_criteria_descriptions = set()
    staff = Staff.objects.get(Account_id=request.user)
    course = Course.objects.get(Course_id=course_id)
    instructor = Instructor.objects.get(Instructor_id=instructor_id)
        # Find the latest term where evaluation is not done
    term = Term.objects.filter(Courses_Given=course, EvaluationDone=False).order_by('-Year', 'Season').first()

    if not term:
        messages.warning(request, 'Course evaluation is already completed for all terms.')
        return redirect('evaluate')  # Redirect to home or another page
    all_criteria_objects = EvaluationCriteria.objects.get(Evaluator='StaffMember')  # Adjust based on your criteria
    # all_criteria_objects = EvaluationCriteria.objects.all()
    # Collect all distinct criteria sections using Python
    all_criteria_data = all_criteria_objects.Criteria_data.all()
    all_criteria = []
    criteria_sections = []
    for criteria_object in all_criteria_data:
        criteria = Criteria.objects.get(Criteria_id= criteria_object.Criteria_id) 
        if criteria.Section not in  criteria_sections :
            all_criteria.append(criteria)
            criteria_sections.append(criteria.Section)
        print("criteria section" , criteria.Section )
    print("all sectins are ", all_criteria)
    if request.method == 'POST':
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
        print("evaluation resullt",evaluation_result)     
        if evaluation_result and evaluated_criteria_descriptions == all_criteria_descriptions:
            result_instance, created = StaffEvaluationResult.objects.get_or_create(
                Staff_id=staff,
                Course_id=course,
                Instructor_id=instructor,
                CourseType = course_type,
                Term_id=term,
                defaults={'EvaluationResult': evaluation_result, 'EvaluationDone': True}
            )

            if not created:
                messages.error(request, 'Please evaluate all sections!')
            messages.success(request, 'You have completed Evaluation for course '+ course.CourseName) 
            return redirect('evaluate_staff')  # Redirect to home or another page after evaluation
        else:
            messages.error(request, 'Please evaluate all criteria descriptions before submitting!')
    context = {
        'course':course,
        'criteria_data': all_criteria_data, 
        'active_page':'evaluation',
        'all_criteria_sections':all_criteria ,
        'instructor':instructor,
        'course_type':course_type,
    }

    return render(request, 'staff/evaluate_course.html', context)

def academicheadHomePage(request):
    context = { 'active_page': 'home',}
    return render(request , 'academichead/academicheadhome.html' , context)