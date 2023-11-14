from django.shortcuts import render

# Create your views here.
def Instructors(request):
    context = {'user':request.user}
    return render(request , 'instructor/instructor.html' , context)