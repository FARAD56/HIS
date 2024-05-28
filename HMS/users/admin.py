from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,ProfileModel

class CustomUserAdmin(UserAdmin):
    # Ensure you include the custom fields in the list display if needed
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('contact', 'dob', 'sex')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ProfileModel)
