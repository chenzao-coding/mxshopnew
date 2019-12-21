# FileName: yunpian
# Author: Tunny
# @time: 2019-12-21 16:48
# Desc: 
import requests
import json


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【慕学生鲜】您的验证码是{}。如非本人操作，请忽略本短信".format(code)
        }
        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        print(re_dict)
        return re_dict


if __name__ == '__main__':
    yun_pian = YunPian('d6c4ddbf50ab36611d2f52041a0b949e')
    yun_pian.send_sms('2019', '15399400517')
