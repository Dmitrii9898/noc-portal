from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AppUser, Role

admin.site.register(Role)


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    list_display = ("username", "full_name", "role", "email", "is_active")
    list_filter = ("role", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Портал", {"fields": ("role", "full_name", "organization", "phone")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Портал", {"fields": ("role", "full_name", "organization", "phone")}),)
