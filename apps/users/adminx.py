# -*- coding: utf-8 -*-
# FileName: adminx
# Author: Tunny
# @time: 2019-10-15 10:53
# Desc:
from users.models import VerifyCode

import xadmin
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '学习商城'
    site_footer = 'aaa@qq.com'
    # menu_style = 'accordion'


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', 'add_time']


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
