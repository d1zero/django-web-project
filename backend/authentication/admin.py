from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.unregister(Group)
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'get_image', 'date_joined', 'last_login', 'is_active', 'is_admin')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login', 'get_image',)
    exclude = ('password', 'token', 'avatar')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

