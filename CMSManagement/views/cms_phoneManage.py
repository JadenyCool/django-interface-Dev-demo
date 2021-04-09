"""
phone management interface
"""

from rest_framework_app_api import response
from rest_framework_app_api.views import APIView
from rest_framework.decorators import api_view
from ..models import PhoneManage

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


# add phone
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def AddPhone(request):
    data = request.data
    device_name = data['dname']
    os_version = data['osVersion']
    type = data['type']
    iemi = data['iemi']
    is_home = data['is_home']
    remarks = data['remarks']
    if (device_name or os_version or type or iemi or is_home) is None:
        return response.APIResponseErrorParams(msg='params cannot be empty', code=101)

    obj, created = PhoneManage.objects.filter(iemi=iemi).get_or_create(dname=device_name, os_version=os_version,
                                                                       type=type, iemi=iemi, is_home=is_home,
                                                                       remarks=remarks)
    return response.APIResponseSuccess(msg="Add phone success")
