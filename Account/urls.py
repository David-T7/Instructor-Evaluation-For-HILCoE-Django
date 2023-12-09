from . import views
from django.urls import path
from .forms import ResetPasswordForm, NewPasswordForm
from django.contrib.auth import views as djangoviews

urlpatterns = [ 
path('login', views.Login , name='login'), 
path('logout' , views.Logout , name='logout') ,
path('editusername' , views.EditUserName , name='editusername' ), 
path('editpassword' , views.EditPassword , name='editpassword'),
path('addrecoveryemail' , views.addRecoveryEmail , name = 'addrecoveryemail'),
path('password-reset/', djangoviews.PasswordResetView.as_view(template_name="reset_password.html", form_class=ResetPasswordForm), name="password_reset"),
path('password-reset/done/', djangoviews.PasswordResetDoneView.as_view(template_name="reset_password_done.html"), name="password_reset_done"),
path('password-reset-confirm/<uidb64>/<token>/', djangoviews.PasswordResetConfirmView.as_view(template_name="reset_password_confirm.html", form_class=NewPasswordForm), name="password_reset_confirm"),
path('password-reset-complete/', djangoviews.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name="password_reset_complete"),
]
