from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import CustomUser, UserFavorite

admin.site.unregister(Group)
admin.site.register(UserFavorite)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, SimpleHistoryAdmin):
    list_display = ('email', 'username', 'get_image', 'date_joined',
                    'last_login', 'is_active', 'is_admin')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login', 'get_image',)
    exclude = ('password', 'token', 'avatar')
    history_list_display = ["status"]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
