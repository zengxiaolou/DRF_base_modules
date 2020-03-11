__author__ = 'ROOT'

from django.conf.urls import url, include


urlpatterns = [
    url(r'^captcha/', include('rest_captcha.urls')),

]