from django.contrib import admin
from .models import User


# Register your models here.
# class MyUserAdmin(admin.ModelAdmin):
#     list_display = ["email", "first_name", "last_name", "id"]


admin.site.register(User)
