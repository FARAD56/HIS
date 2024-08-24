from django.db import models
from users.models import CustomUser
from django.utils import timezone
# Create your models here.
class Todo(models.Model):
    task = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='todos')

    def get_deadline_label(self):
        now = timezone.now()
        deadline_date = self.deadline.date()
        if deadline_date == now.date():
            return "Today"
        elif deadline_date == (now + timezone.timedelta(days=1)).date():
            return "Tomorrow"
        else:
            return self.deadline.strftime("%d %B %Y, %I:%M %p")
        
    def __str__(self):
        return self.task
    
