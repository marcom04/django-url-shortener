from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.core.models import (
    Mapping,
    User,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'last_name', 'first_name', 'is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Name'),
            {
                'fields': ('first_name', 'last_name')
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (
            _('Important dates'),
            {
                'fields': ('last_login',)
            }
        )
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'first_name', 'last_name',
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
    )


@admin.register(Mapping)
class MappingAdmin(admin.ModelAdmin):
    pass
