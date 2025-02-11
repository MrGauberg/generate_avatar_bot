from django.contrib import admin
from django_celery_results.models import TaskResult

@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ("task_id", "status", "date_done", "result")
    search_fields = ("task_id", "status")
