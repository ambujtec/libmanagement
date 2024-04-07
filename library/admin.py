from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Book

# class CustomUserAdmin(UserAdmin):
#     list_display = (
#         'username', 'email', 'first_name', 'last_name', 'usertype'
#         )

admin.site.register(CustomUser)
admin.site.register(Book)