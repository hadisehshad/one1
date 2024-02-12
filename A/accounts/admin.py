from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.models import Group


# Register your models here.

'''@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')'''


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin', 'role_type', 'work_experience')
    list_filter = ('is_admin',)
    fieldsets = (
        ('Main', {'fields': ('email', 'phone_number', 'name', 'family', 'role_type', 'work_experience', 'password')}),
        ('permissions', {'fields': ('is_active', 'is_admin', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'name', 'family', 'role_type', 'work_experience',
                           'password1', 'password2')}),
    )

    search_fields = ('email', 'name', 'family')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
#admin.site.register(Role)
