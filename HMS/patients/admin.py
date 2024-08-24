from django.contrib import admin
from .models import Todo
# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    def user_name(self, obj):
        return obj.user.full_name

    list_display = ('id','user_name', 'task','deadline','is_completed','created_at')  
    search_fields = ('id', 'user') 

admin.site.register(Todo, TodoAdmin)
