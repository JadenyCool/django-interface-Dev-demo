import json
from functools import wraps

from django.http import HttpResponse
from utils.AESUtils import AEScrypt
from .models import authToken


# 后台用户登录
# def cms_login_required(func):
#     @wraps(func)
#     def inner(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return func(request, *args, **kwargs)
#         else:
#             data = {"code": 101, "msg": "Not login system"}
#             return HttpResponse(json.dumps(data))
#
#     return inner

def cms_login_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        getToken = request.META.get('HTTP_TOKEN')
        if str(request.user) == AEScrypt(str(request.user)).aes_decrypt(getToken):
            return func(request, *args, **kwargs)
        else:
            data = {"code": 101, "msg": "Not login system"}
            return HttpResponse(json.dumps(data))

    return inner
