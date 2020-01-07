# Copyright @ 2020 China Mobile (SuZhou) Software Technology Co.,Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from res.biz.vnfs_get import GetVnfsService
from res.pub.exceptions import VNFRESException
from res.pub.utils.syscomm import fun_name
from res.resources.serializers import VnfInfoSerializer, VnfsInfoSerializer
from res.resources.views.views import view_safe_call_with_log

logger = logging.getLogger(__name__)


class GetVnfView(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: VnfInfoSerializer(),
            status.HTTP_404_NOT_FOUND: 'Vnf does not exist',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request, vnf_instance_id):
        logger.debug("[%s]vnf_inst_id=%s", fun_name(), vnf_instance_id)

        resp_data = GetVnfsService().get_vnf(vnf_instance_id)

        vnf_info_serializer = VnfInfoSerializer(data=resp_data)
        if not vnf_info_serializer.is_valid():
            raise VNFRESException(vnf_info_serializer.errors)

        return Response(
            data=resp_data,
            status=status.HTTP_200_OK
        )


class GetVnfsView(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: VnfsInfoSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request):
        a = 9
        return GetVnfsService().get_vnfs()
