from django.shortcuts import render

# Create your views here.
def homepage(request): 
    return render(request , 'homepage.html')

def staffhomepage(request): 
    return render(request , 'staffhomepage.html')