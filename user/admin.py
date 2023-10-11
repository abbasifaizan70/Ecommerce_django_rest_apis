from django.contrib import admin

# Register your models here.
from .models import User

admin.site.register(User)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ["first_name", "last_name", "email"]
