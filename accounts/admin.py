from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailConfirm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_active')
    list_filter   = ('is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    
    
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone', 'address', 'avatar')}),
    )


@admin.register(EmailConfirm)
class EmailConfirmAdmin(admin.ModelAdmin):
    list_display = ('user', 'code')
    search_fields = ('user__username', 'user__email')
