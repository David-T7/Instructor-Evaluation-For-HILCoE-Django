from django.contrib import admin
from Account.forms import CustomUserCreationForm
from .models import  StudentInfo , Account
from django.contrib.auth.admin import UserAdmin
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = Account
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','password1', 'password2','Role','email')}
        ),
    )
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','password','Role','email')}
        ),
    )

admin.site.register(StudentInfo)
admin.site.register(Account , CustomUserAdmin)
