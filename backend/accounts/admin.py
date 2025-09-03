from django.contrib import admin
from .models import CustomUser,Otp
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateRangeFilterBuilder
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','phone_no','is_active','staff','admin','referrer_user','is_remove','last_login','create_time','update_time')
    search_fields = ('username', 'email','phone_no','is_active','staff','admin','referrer_user','is_remove','last_login','create_time','update_time')
    list_filter = ('is_active','staff','admin','is_remove',('last_login',DateRangeFilterBuilder()),('create_time',DateRangeFilterBuilder()),('update_time',DateRangeFilterBuilder()))
    ordering = ('username',)

    #Managing admin panel delete acton/button
    def has_delete_permission(self, request, obj=None):
        return True 
    
    #Converting to ReadOnly Fields
    readonly_fields = ('username', 'email','phone_no','last_login','create_time','update_time')

class OtpAdmin(admin.ModelAdmin):
    list_display = ('email','otp','purpose','ttl','is_remove','update','create_time')
    search_fields = ('email','otp','purpose','ttl','is_remove','update','create_time')
    list_filter = ('purpose',('ttl',DateRangeFilterBuilder()),'is_remove',('update',DateRangeFilterBuilder()),('create_time',DateRangeFilterBuilder()))
     
    #Managing admin panel delete acton/button
    def has_delete_permission(self, request, obj=None):
        return False 
    
    #Converting to ReadOnly Fields
    readonly_fields = ('email','otp','purpose','ttl','update','create_time')

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Otp ,OtpAdmin)





