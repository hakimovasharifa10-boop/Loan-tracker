from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display  = ('title', 'user', 'icon', 'target_amount', 'current_amount', 'target_date', 'status')
    list_filter   = ('status', 'target_date')
    search_fields = ('title', 'user__username', 'description')
    date_hierarchy = 'target_date'
