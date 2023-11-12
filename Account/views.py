from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from Account.models import Account
from Account.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib import  messages
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib.auth import update_session_auth_hash



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


def Logout(request):
    logred = '/login/' + request.user.Role  # getting the redirection path for every role
    logout(request)
    messages.info(request, 'Successfuly Logged out!')    
    return redirect(logred)

def Userstate(request):  # for getting the state of the user 
    state = request.user
    account = Account.objects.get(id=state.id) 
    context={'account':account}
    return context

def EditUserName(request):
    state = request.user # hodling the state of the user
    account = Userstate(request)['account']
    form= CustomUserChangeForm(instance=state)  # using form created in forms.py

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=state)
        if (form.is_valid()):
            try:
                form.save()
                messages.success(request,'Account updated successfuly')
            except:
                None
        request.user.save() # saving the state of the user after it is updated 
    context = {'form': form , 'account':account , 'sender':'username'}
    if(request.user.Role.lower() == 'student'):
        return render(request, 'student/editusername.html', context)

def EditPassword(request):
    account = Userstate(request)['account']
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if (form.is_valid()):
            try:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.error(request,'Password Was  Updated Successfuly')

            except:
                messages.error(request,'Error occured during updating password')
        else:
                messages.error(request,'please input correct information')
        request.user.save()
    context= {'form':form , 'account':account , 'sender':'password'}
    if(request.user.Role.lower() == 'student'):
        return render(request, 'student/editpassword.html', context)
   
