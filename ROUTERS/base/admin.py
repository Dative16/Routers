from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import *


# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_of_joined', 'is_active',)
    list_display_links = ('email', 'first_name', 'last_name', 'username')
    readonly_fields = ('last_login', 'date_of_joined')
    ordering = ('-date_of_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    search_fields = ('email', 'first_name', 'last_name', 'username')



admin.site.register(Account, AccountAdmin)
