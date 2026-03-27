from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin
from apps.users.models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email', 'avatar', 'active_farm')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Role'), {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role'),
        }),
    )

    list_display = ("email", "first_name", "last_name", "role", "is_superuser", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    # email is used instead of username
    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj)

    def get_add_fieldsets(self, request):
        return self.add_fieldsets



admin.site.register(Profile)