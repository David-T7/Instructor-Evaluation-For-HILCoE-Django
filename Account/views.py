from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
import Account
from Account.forms import CustomUserCreationForm
from django.contrib import  messages

# Create your views here.
def Login(request , role):          # function based view for handling user login
    form = CustomUserCreationForm()
    if request.method == 'POST':
        username = request.POST['username'].lower()      # making sure the user name is in lowercase 
        password = request.POST['password1']
        try:
            user = authenticate(request=request, username=username, password=password , Role  =role)   # full user authenticaton including role
            if user is not None:
                login(request, user) 
                if(role.lower() =='student'):    
                    return redirect('studnet')  # redircting to other page after login
            else:
                login(request, user , backend='django.contrib.auth.backends.ModelBackend')
        except:
            try:
                testusername = Account.objects.get(username = username)
                messages.error(request, 'Incorrect Password')
            except:
                messages.error(request, 'Username doestnot exist')
    return render(request, 'login.html',{'Role':role,'form':form})  