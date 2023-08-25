from django.contrib import admin

# Register your models here.
from todolist_app.models import TaskList

admin.site.register(TaskList)