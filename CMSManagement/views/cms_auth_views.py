from django.contrib import auth
from django.db.models import Q
from django.forms import model_to_dict

from rest_framework.decorators import api_view
from rest_framework_app_api import response
from rest_framework_app_api.views import APIView
from rest_framework_jwt.settings import api_settings
from ..models import UserInfo
# from django.core import serializers
# from rest_framework import serializers
# import json
from ..models import authToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


# CMS 登录 session 认证
# class LoginView(APIView):
#     def post(self, request):
#         login_data = request.data
#         username = login_data['username']
#         password = login_data['password']
#         user = auth.authenticate(request, username=username, password=password)
#         if user:
#             auth.login(request, user)
#             data = UserInfo.objects.filter(username=request.user)
#
#             # 两种方式：
#             # 方法一：使用model_to_dict
#             # print(model_to_dict(data[0], fields=('zh_name', 'username', 'phone', 'email')))
#             # 显示多条数据的时候：data = UserInfo.objects.all()
#             # result = []
#             # for i in range(len(data)):
#             #     result.append(model_to_dict(data[i], fields=('zh_name', 'username', 'phone', 'email')))
#             # print(result)
#             # result = model_to_dict(data[0], fields=('zh_name', 'username', 'phone', 'email', 'last_login'))
#             result = model_to_dict(data[0], exclude=('password', 'groups', 'user_permissions'))
#             return response.APIResponseSuccess(msg='success', data=result)
#
#             # 方法二：使用serializers
#             # result_serialize = serializers.serialize('json', data, fields=('zh_name', 'username', 'phone', 'email'))
#             # 查询结果序列化，这个时候，result_serialize 还是字符类型，需要json.loads转化为json格式
#             # 不转化为json格式也是可以的直接返回数据的，但是返回的数据没有经过过滤的
#             # return HttpResponse(result_serialize, "application/json")
#             # return response.APIResponseSuccess(msg="success", data=json.loads(result_serialize), content_type="application/json")
#         else:
#             return response.APIResponseErrorParams(msg="fail")

# https://blog.csdn.net/qq_45618388/article/details/106069094
# token认证
# JWT在postman中的使用：
# 在headers 中增加：key: Authorization   value: JWT +生成的token, 例如：JWT adsfads1232131
class LoginView(APIView):
    def post(self, request):
        login_data = request.data
        username = login_data['username']
        password = login_data['password']

        if username and password:
            user = auth.authenticate(request, username=username, password=password)
            if user:
                # auth.login(request, user)
                # token = AEScrypt(str(user)).aes_encrypt()
                # print(request.user.id)
                # authToken.objects.filter(user_id=request.user.id).get_or_create(key=token, user_id=request.user.id)
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                userinfo = UserInfo.objects.filter(username=user)
                data = model_to_dict(userinfo[0], exclude=("password", 'groups',))
                data['token'] = token
                return response.APIResponseSuccess(msg="Login Success", data=data)
            return response.APIResponseErrorParams(msg="user is not exist", code=301)
        return response.APIResponseErrorParams(msg="username or password is None", code=300)


# CMS注销, 后台不做处理，该功能作废弃
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def Logout(request):
    token = request.META.get('HTTP_TOKEN')
    user = authToken.objects.filter(key=token)
    if user:
        user.delete()
        return response.APIResponseSuccess(msg="Logout success")
    return response.APIResponseErrorParams(msg="{} is not exist".format(user), code=309)


# CMS 注册
@api_view(['POST'])
def Register(request):
    register_data = request.data
    username = register_data['username']
    zh_name = register_data['zh_name']
    password = register_data['password']
    phone = register_data['phone']
    email = register_data['email']

    # 判断是否为空:
    if (username or zh_name or password or phone or email) is None:
        return response.APIResponseErrorParams(msg="user info cannot be empty", code=305)

    user = UserInfo.objects.filter(Q(username=username) | Q(email=email) | Q(phone=phone) | Q(zh_name=zh_name)).first()
    if user:
        return response.APIResponseErrorParams(msg="user info has been already, please changing it", code=306)
    else:
        userinfo = UserInfo.objects.create_user(username=username, password=password, phone=phone, email=email,
                                                zh_name=zh_name,
                                                detail="cms")
        userinfo.save()
    return response.APIResponseSuccess(msg="user create success")


# 重置密码
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def RestPsw(request):
    data = request.data
    oldpsw = data['oldpassword']
    newpsw1 = data['newpassword1']
    newpsw2 = data['newpassword2']
    if (oldpsw or newpsw1 or newpsw2) is None:
        return response.APIResponseErrorParams(msg="password cannot empty", code=307)
    if newpsw1 != newpsw2:
        return response.APIResponseErrorParams(msg="The two passwords do not match", code=308)

    user = request.user
    if user.check_password(oldpsw):
        user.set_password(newpsw1)
        user.save()
        return response.APIResponseSuccess(msg="Password modified successfully")
    else:
        return response.APIResponseErrorParams(msg="Incorrectly old password", code=310)


# 更新手机号
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def updatePhone(request):
    data = request.data
    newphone = data['phonenumber']
    if newphone is not None and len(newphone) < 11:
        return response.APIResponseErrorParams(msg="Incorrectly phone number", code=311)
    else:
        user = request.user
        if user:
            user.phone = newphone
            user.save()
            return response.APIResponseSuccess(msg='success')


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def test(request):
    token = request.META.get('HTTP_TOKEN')
    data = {"test": token}
    return response.APIResponse(msg="test success", data=data)
