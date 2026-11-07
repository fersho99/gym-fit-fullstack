from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin de usuarios: conserva el formulario seguro de contraseña de Django."""

    list_display = ('email', 'username', 'first_name', 'last_name', 'telefono', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'telefono')
    ordering = ('email',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Datos del gimnasio', {'fields': ('telefono',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Datos del gimnasio', {'fields': ('email', 'telefono')}),
    )
