from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,ProfileModel

class CustomUserAdmin(UserAdmin):
    # Ensure you include the custom fields in the list display if needed
    list_display = ('profile_id', 'email', 'first_name', 'is_superuser', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('contact', 'dob', 'sex')}),
    )


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('full_name','user','triage')

    def full_name(self, obj):
        return obj.user.full_name

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ProfileModel,ProfileModelAdmin)