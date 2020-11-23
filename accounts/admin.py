from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UpdateUserForm, AddUserForm
from .models import User


class UserAdmin(BaseUserAdmin):
	form = UpdateUserForm
	add_form = AddUserForm

	list_display = ('phone', 'username', 'email', 'name', 'date_joined', 'is_staff')
	list_filter = ('is_staff', 'is_active')
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('name', 'phone', 'gender')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'notification_level', 'groups', 'user_permissions')}),
	)
	add_fieldsets = (
		(
			None,
			{
				'classes': ('wide',),
				'fields': (
					'email', 'name', 'phone', 'gender', 'notification_level'
				)
			}
		),
	)
	search_fields = ('email', 'name', 'phone')
	ordering = ('name',)
	filter_horizontal = ('user_permissions', 'groups')


admin.site.register(User, UserAdmin)