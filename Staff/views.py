from django.shortcuts import redirect, render
from Course.models import Course, CourseInstructor, Term
from Evaluation.models import Criteria, EvaluationCriteria
from Instructor.models import Instructor
from Student.models import StudentCourseEnrollment, StudentEvaluationResult
from Student.forms import GeneralReportForm
from .models import Staff, StaffEvaluationResult
from django.contrib import  messages
from django.utils import timezone
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
# Create your views here.
def stafflandingpage(request): 
    return render(request , 'stafflandingpage.html')
def staffHomePage(request):
    term = None
    try:
        term = Term.objects.get(EvaluationDone = False)
    except:
        term = None
    evaluation_started = False
    evaluation_ended = False
    if(term.Evaluation_Start_Date <= timezone.now()):
        print('evaluation started')
        evaluation_started = True
    if(term.Evaluation_End_Date > timezone.now()):
        print('evaluation ended')
        evaluation_ended = True
    context = { 'active_page': 'home', 'term':term , 'evaluation_started':evaluation_started , 'evaluation_ended':evaluation_ended }
    return render(request , 'staff/staffhome.html' , context)

def staff_evaluate_page(request):
    term = None
    try:
        term = Term.objects.get(EvaluationDone = False)
    except:
        term = None
    evaluation_started = False
    evaluation_ended = False
    if(term.Evaluation_Start_Date <= timezone.now()):
        print('evaluation started')
        evaluation_started = True
    if(term.Evaluation_End_Date > timezone.now()):
        print('evaluation ended')
        evaluation_ended = True
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
        'evaluation_started':evaluation_started,
        'evaluation_ended':evaluation_ended,
        
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
    desired_order = ['Timely Grade Submission' , 'Accuracy of Grade Records' , 'Grade Appeals Process' , 'Grade Change Procedures']
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
    criteria_sections.sort(key=lambda x: desired_order.index(x.Section))
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
        print("evaluation resullt",evaluation_result)
        additional_comment = request.POST.get('additional_comment')     
        if evaluation_result and evaluated_criteria_descriptions == all_criteria_descriptions:
            result_instance, created = StaffEvaluationResult.objects.get_or_create(
                Staff_id=staff,
                Course_id=course,
                Instructor_id=instructor,
                CourseType = course_type,
                Term_id=term,
                AdditionalComment = additional_comment, 
                defaults={'EvaluationResult': evaluation_result, 'EvaluationDone': True}
            )

            if not created:
                messages.error('Please evaluate all criteria descriptions before submitting!')
                error_occured = True
            else:
                messages.success(request, 'You have completed Evaluation for course '+ course.CourseName) 
                return redirect('evaluate_staff')  # Redirect to home or another page after evaluation
        else:
            messages.error(request, 'Please evaluate all criteria descriptions before submitting!')
            error_occured = True

    context = {
        'course':course,
        'criteria_data': all_criteria_data, 
        'active_page':'evaluation',
        'all_criteria_sections':all_criteria ,
        'instructor':instructor,
        'course_type':course_type,
        'criteria_results' : criteria_results,
        'error_occured'  :error_occured,
    }

    return render(request, 'staff/evaluate_course.html', context)

def academicheadHomePage(request):
    term = None
    try:
        term = Term.objects.get(EvaluationDone = False)
    except:
        term = None
    evaluation_started = False
    evaluation_ended = False
    if(term.Evaluation_Start_Date <= timezone.now()):
        print('evaluation started')
        evaluation_started = True
    if(term.Evaluation_End_Date > timezone.now()):
        print('evaluation ended')
        evaluation_ended = True
    context = { 'active_page': 'home', 'term':term , 'evaluation_started':evaluation_started , 'evaluation_ended':evaluation_ended}
    return render(request , 'academichead/academicheadhome.html' , context)

# def render_to_pdf(template_src, context_dict={}):
# 	template = get_template(template_src)
# 	html  = template.render(context_dict)
# 	result = BytesIO()
# 	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
# 	if not pdf.err:
# 		return HttpResponse(result.getvalue(), content_type='application/pdf')
# 	return None

def ViewPDF(templatename , data):
		pdf = render_to_pdf('academichead/'+templatename, data)
		return HttpResponse(pdf, content_type='application/pdf')

def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def DownloadPDF(templatename, data, filename):
    pdf = render_to_pdf('academichead/'+templatename, data)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
        return response

    # Handle the case where PDF generation failed
    return HttpResponse("PDF generation failed", status=500)
def generalEvaluationReport(request , type):
    evaluations = None
    term = None
    evaluator = None
    course_type = None
    if request.method == 'POST':
        print("in post before evaluting form" , request.POST)
        query = request.POST
        query_dic = {'term':'Term_id'}
        if query:
            query_params = {}
            if query['evaluator']:
                evaluator = query['evaluator']
            else:
                evaluator = 'both'
            if query['course_type']:
                course_type = query['course_type']
            print('form cleaned data is ' , query.items())
            # Check each form field and add it to the query_params if it's not empty
            for field_name, value in query.items():
                if value and field_name in query_dic:
                    if field_name == 'term':
                        value_object = Term.objects.get(Season = value.split()[0] ,Year=value.split()[1]) 
                        if value_object:
                            term = value_object    
  
            desired_order = []
    
            if evaluator == 'Student':
                evaluations = StudentEvaluationResult.objects.filter(
                Term_id= term , 
                EvaluationDone=True ,
                CourseType = course_type
                    )
                desired_order = ['Course Organization', 'Knowledge of the subject matter', 'Teaching Methods',
                    'Student Involvement', 'Evaluation Methods' , 'Personality Traits' , 'Availability and Support']
            elif evaluator == 'Staff':
                evaluations = StaffEvaluationResult.objects.filter(
                Term_id=term,
                EvaluationDone=True ,
                CourseType = course_type
                    )
                desired_order = ['Timely Grade Submission' , 'Accuracy of Grade Records' , 'Grade Appeals Process' , 'Grade Change Procedures']
            criteria_average_details = []
            criteria = []
            criteria_category = {}
            criteria_sections = []
            criteria_average_Scores = []
   
            if evaluations:
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
                print ('before soring criteria category is ' , criteria_category)
                criteria_sections  = sorted(criteria_sections, key=lambda x: desired_order.index(x) if x in desired_order else float('inf'))
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
                    print('criteria category before sorting is ' , criteria_category)
                    print ('criteria_average_Scores is ' , criteria_average_Scores)               
                context = {'criteria_average_Scores':criteria_average_Scores  , 
                        'criteria_sections':criteria_sections , 
                        'evaluations':evaluations, 
                         'active_page':'geneal_report',
                         'evaluator':evaluator ,
                         'term':term ,
                         'course_type':str.title(course_type)
                    }
                if(type == 'view'):    
                    return render (ViewPDF('generalreport.html',context))
                elif (type == 'download'):
                    print('downloading')
                    return ViewPDF('generalreport.html' , context)
                    # return DownloadPDF('generalreport.html' , context , 'evaluation_report')
            else:
                messages.error(request, 'No result found!')
                return redirect('general_evaluation_report')    
    else:
        terms = Term.objects.all()
        form = GeneralReportForm
        context = {'form':form , 'active_page': 'general_report' , 'terms':terms}
        return render(request, 'academichead/evaluationreportpage.html' , context )    
