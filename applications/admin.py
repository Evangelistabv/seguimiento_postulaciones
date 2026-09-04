from django.contrib import admin
from .models import Activity, JobApplication


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "status", "priority", "applied_on", "updated_at")
    list_filter = ("status", "priority", "work_mode")
    search_fields = ("title", "company", "source")
    inlines = [ActivityInline]
