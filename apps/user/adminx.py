#_*_ coding:utf-8 _*_
__author__ = 'Harryue'
__date__ = '2018/6/28 PM3:56'

import xadmin
from user.models import UserProfile, EmailVerifyRecord

# class UserProfileAdmin(object):
#     list_display = ('nick_name','gender','email','mobile')
#     search_fields = ('nick_name','gender','email','mobile')

# xadmin.site.register(UserProfile,UserProfileAdmin)


class EmailVerifyRecordAdmin(object):
    list_display = ('email', 'code', 'send_type', 'send_time')
    search_fields = ('email')
    list_filter = ('send_type', 'is_valid')

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)

from xadmin import views

class GlobalSetting(object):
    site_title = 'bibibi'  # 设置头标题
    site_footer = 'bibibi'  # 设置脚标题

    menu_style = 'accordion'  # 菜单课收缩

xadmin.site.register(views.CommAdminView, GlobalSetting)


class BaseSetting(object):
    enable_themes = False  # 设置可更换主题
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)