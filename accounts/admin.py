from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Roles', {'fields': ('is_admin', 'is_doctor', 'is_patient')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'phone_number',
                'password1',
                'password2',
                'is_admin',
                'is_doctor',
                'is_patient',
                'is_staff',
            ),
        }),
    )

    list_display = (
        'username',
        'email',
        'is_admin',
        'is_doctor',
        'is_patient',
        'is_superuser',
    )

    search_fields = ('username', 'email')
    ordering = ('username',)