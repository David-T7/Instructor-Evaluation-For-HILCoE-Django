from datetime import datetime, timezone
from os import path
from django.contrib import admin
from django.shortcuts import render
from .models import Student, StudentEvaluationResult
from django.conf import settings
import os

from django.contrib import admin
from django import forms
from openpyxl import load_workbook
from .models import StudentCourseEnrollment, Student, Course, Term

class PopulateFromExcelForm(forms.Form):
    file = forms.FileField()

class StudentCourseEnrollmentAdmin(admin.ModelAdmin):
    actions = ['populate_from_excel']
    change_list_template = 'admin/populate_from_excel_change_list.html'

    def populate_from_excel(self, request):
        form = None
        opts = admin.site._registry[StudentCourseEnrollment].model._meta
        print("in populate ")
 
        if '_apply' in request.POST:
            print("in apply")
            form = PopulateFromExcelForm(request.POST, request.FILES)
            print("in apply")
            if form.is_valid():
                file_path = self.handle_uploaded_file(request.FILES['file'])
                print("file is valid")    
                # Load the Excel file
                wb = load_workbook(file_path)
                sheet = wb.active
                   
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    student_id, course_id = row
                        
                    student = Student.objects.get(Student_id=student_id)
                    course = Course.objects.get(Course_id=course_id)
                    term = Term.objects.last()

                    enrollment, created = StudentCourseEnrollment.objects.get_or_create(
                        student=student,
                        course=course,
                        term=term,
                        defaults={'enrolled': True}
                    )

                self.message_user(request, f'StudentCourseEnrollment instances populated from Excel file: {file_path}')
        else:
            
            form = PopulateFromExcelForm()

        return render(request, 'admin/populate_from_excel.html', {'form': form ,'opts': opts})

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('populate_from_excel/', self.populate_from_excel, name='populate_from_excel'),
        ]
        return custom_urls + urls

    

    def handle_uploaded_file(self, file):
        destination_path = os.path.join(settings.MEDIA_ROOT, file.name)
    
        # Add a timestamp to the filename to avoid overwriting
        timestamped_filename = f"{os.path.splitext(file.name)[0]}_{datetime.now().strftime('%Y%m%d%H%M%S')}{os.path.splitext(file.name)[1]}"
        destination_path = os.path.join(settings.MEDIA_ROOT, timestamped_filename)

        with open(destination_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return destination_path


    populate_from_excel.short_description = 'Populate StudentCourseEnrollment from Excel'

# Register your models here.
admin.site.register(Student)
# Register the model admin with the admin site
admin.site.register(StudentCourseEnrollment, StudentCourseEnrollmentAdmin)
admin.site.register(StudentEvaluationResult)
