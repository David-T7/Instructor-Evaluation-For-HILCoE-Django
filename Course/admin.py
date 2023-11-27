from django.contrib import admin
from .models import Course ,Term , CourseInstructor
# Register your models here.
admin.site.register(Course)
admin.site.register(Term)
admin.site.register(CourseInstructor)