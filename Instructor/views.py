from django.shortcuts import redirect, render

from Course.models import Course, CourseInstructor, Term
from Evaluation.models import Criteria, EvaluationCriteria
from Staff.models import PeerEvaluationResult
from Student.models import StudentCourseEnrollment
from .models import Instructor
from django.contrib import  messages
# Create your views here.
def Instructors(request):
    context = {'user':request.user}
    return render(request , 'instructor/instructor.html' , context)
def InstructorHomePage(request):
    instructor = Instructor.objects.get(Account_id = request.user)
    context = { 'active_page': 'home', 'instructor':instructor}
    return render(request , 'instructor/instructorhome.html' , context)
def instructor_evaluate_page(request):
    term = Term.objects.last()
    instructor = Instructor.objects.get(Account_id=request.user)
    student_enrollments = StudentCourseEnrollment.objects.filter(term=term)
    instructor_evaluation_result = PeerEvaluationResult.objects.filter(Evaluator_Instructor_id = instructor)
    evaluated_courses_types = []
    evaluated_instructors = []
    course_instructors = []    
    if instructor_evaluation_result:
        for instructor_evaluation in instructor_evaluation_result:
            evaluated_instructors.append(instructor_evaluation.Instructor_id.Instructor_id)
            evaluated_courses_types.append(instructor_evaluation.CourseType)
    courses_data = []
    for enrollment in student_enrollments:
        instructor_courses = CourseInstructor.objects.filter(Course = enrollment.course , Instructors = instructor )
        instructors_data = []
        for courses in instructor_courses:
            shared_courses = CourseInstructor.objects.filter(Course = courses.Course)
            if(shared_courses.__len__() > 1):
                print("shared course lenght ", shared_courses.__len__()) 
                for shared_course in shared_courses:
                    if  shared_course.Instructors.Instructor_id != instructor.Instructor_id :
                        course_instructors.append(shared_course)
                        instructor_info = {
                            'name': f'{shared_course.Instructors.FirstName} {shared_course.Instructors.LastName}',
                            'title': shared_course.Instructors.Title,
                            'instructor_id':shared_course.Instructors.Instructor_id , 
                            'profile_pic': shared_course.Instructors.ProfilePic.url if shared_course.Instructors.ProfilePic else None,
                                }
                        instructors_data.append(instructor_info)

                        course_data = {
                            'course_name': shared_course.Course.CourseName,
                            'course_id':shared_course.Course.Course_id,
                            'instructors': instructors_data,
                            'evaluate_url': f'/evaluate/{enrollment.id}/',  # Replace with the actual URL for evaluation
                            }
                        courses_data.append(course_data)
    print("shared course instructors " , course_instructors)
    context = {
        'courses_data': courses_data,
        'term': term,
        'active_page':'evaluation',
        'instructor':instructor,
        'evaluatorinstructor':instructor,
        'evaluated_courses_types':evaluated_courses_types,
        'course_instructors':course_instructors,
        'evaluated_instructors':evaluated_instructors,
    }

    return render(request, 'instructor/evaluate.html', context)


def instructor_evaluate_course(request, evaluator_instructor_id, course_id, evaluatee_instructor_id , course_type):
    evaluationMapping= {'Excellent':5,'Very Good':4,'Good':3,'Poor':2,'Very Poor':1}
    evaluated_criteria_descriptions = set()
    evlauator_instructor = Instructor.objects.get(Account_id=request.user)
    course = Course.objects.get(Course_id=course_id)
    evaluatee_instructor = Instructor.objects.get(Instructor_id=evaluatee_instructor_id)
        # Find the latest term where evaluation is not done
    term = Term.objects.filter(Courses_Given=course, EvaluationDone=False).order_by('-Year', 'Season').first()

    if not term:
        messages.warning(request, 'Course evaluation is already completed for all terms.')
        return redirect('evaluate')  # Redirect to home or another page
    all_criteria_objects = EvaluationCriteria.objects.get(Evaluator='Instructor')  # Adjust based on your criteria
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
            result_instance, created = PeerEvaluationResult.objects.get_or_create(
                Evaluator_Instructor_id=evlauator_instructor,
                Course_id=course,
                Instructor_id=evaluatee_instructor,
                CourseType = course_type,
                Term_id=term,
                defaults={'EvaluationResult': evaluation_result, 'EvaluationDone': True}
            )

            if not created:
                messages.error(request, 'Please evaluate all sections!')
            messages.success(request, 'You have completed Evaluation for course '+ course.CourseName) 
            return redirect('evaluate_instructor')  # Redirect to home or another page after evaluation
        else:
            messages.error(request, 'Please evaluate all criteria descriptions before submitting!')
    context = {
        'course':course,
        'criteria_data': all_criteria_data, 
        'all_criteria_sections':all_criteria ,
        'active_page':'evaluation',
        'instructor':evlauator_instructor,
        'evaluateeinstructor': evaluatee_instructor,
        'course_type':course_type,
    }

    return render(request, 'instructor/evaluate_course.html', context)