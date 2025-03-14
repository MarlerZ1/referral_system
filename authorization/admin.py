from django.contrib import admin

from authorization.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', "email", "is_staff"]