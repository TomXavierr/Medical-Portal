from django.contrib import admin
from .models import UserAccount
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class AccountAdmin(UserAdmin):
    list_display     = ('email', 'username', 'first_name', 'is_doctor', 'is_patient')
    search_fields    = ('email', 'username')
    readonly_fields  = ('id',)
    
    filter_horizontal = ()
    list_filter       = ()
    fieldsets         = ()
    
admin.site.register(UserAccount, AccountAdmin),