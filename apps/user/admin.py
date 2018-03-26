from django.contrib import admin

# Register your models here.

from user.models import UserProfile, EmailVerifyRecord

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('nick_name','gender','email','mobile')
    search_fields = ('nick_name','gender','email','mobile')

admin.site.register(UserProfile,UserProfileAdmin)

class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'send_code', 'send_code')
    # search_fields = ('email', 'code', 'send_code', 'send_code')

admin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)