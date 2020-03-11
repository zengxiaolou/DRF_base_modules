__author__ = 'ROOT'
import re
import requests
from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


User = get_user_model()


def generate_code():
    """
    生成6位数字的验证码
    :return:
    """
    seeds = "1234567890"
    random_str = []
    for i in range(6):
        random_str.append(choice(seeds))

    return "".join(random_str)


def jwt_response_payload_handler(token, user=None, request=None):
    """
    为返回的结果添加用户相关信息
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'token': token,
        'username': user.username,
        'id': user.id,
    }


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class TencentSendSms(object):
    """
    腾讯发送短信
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.tencentcloudapi.com/"

    def send_sms(self, code, mobile):
        text = '?Action=SendSms&PhoneNumberSet.0=+86{mobile}&TemplateID=1234&Sign=云动&TemplateParamSet.0={code}' \
               '&SmsSdkAppid{api_key}'.format(mobile=mobile, code=code, api_key=self.api_key)
        response = requests.get(self.single_send_url + text)
        return

