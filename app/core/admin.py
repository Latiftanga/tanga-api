"""Django admin Customization."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define teh admin page for users"""
    ordering = ['email']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_admin',
                    'is_teacher',
                    'is_student',
                    'is_guardian',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide', ),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                    'is_admin',
                    'is_teacher',
                    'is_student',
                    'is_guardian',
                    'is_superuser',
                )
            }
        ),
    )


admin.site.register(models.User, UserAdmin)
