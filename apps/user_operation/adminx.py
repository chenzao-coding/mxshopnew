# -*- coding: utf-8 -*-
# FileName: adminx
# Author: Tunny
# @time: 2019-10-15 11:11
# Desc:
from user_operation.models import UserFav, UserLeavingMessage, UserAddress

import xadmin


class UserFavAdmin(object):
    list_display = ['user', 'goods', "add_time"]


class UserLeavingMessageAdmin(object):
    list_display = ['user', 'message_type', "message", "add_time"]


class UserAddressAdmin(object):
    list_display = ["signer_name", "signer_mobile", "district", "address"]


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
