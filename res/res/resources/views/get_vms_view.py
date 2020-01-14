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
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from res.resources.serializers import VmInfoSerializer
from res.resources.views.base_view import view_safe_call_with_log
from res.biz.vms_get import GetVmsService
logger = logging.getLogger(__name__)


class GetVmsView(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: VmInfoSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request, vnf_instance_id):
        return GetVmsService().get_vms(vnf_instance_id)
