from .models import ProUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

class ProUserAdmin(UserAdmin):
    add_form = UserCreationForm
    model = ProUser
    list_display = ('username', 'email', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'role', 'invitation_code')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'invitation_code', 'is_staff', 'is_superuser', 'groups')}
        ),
    )

admin.site.register(ProUser, ProUserAdmin)
admin.site.unregister(Group)
