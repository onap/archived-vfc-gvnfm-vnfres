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
import traceback

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from res.pub.exceptions import VNFRESException
from res.pub.exceptions import NotFoundException
from res.pub.utils.syscomm import fun_name
from res.pub.database.models import NfInstModel
from res.pub.database.models import StorageInstModel
from res.pub.database.models import NetworkInstModel
from res.pub.database.models import VLInstModel
from res.pub.database.models import VNFCInstModel
from res.pub.database.models import VmInstModel
from res.pub.database.models import FlavourInstModel
from res.pub.database.models import SubNetworkInstModel
from res.pub.database.models import CPInstModel
from res.resources.serializers import VolumeInfoSerializer
from res.resources.serializers import CpsInfoSerializer
from res.resources.serializers import SubnetInfoSerializer
from res.resources.serializers import NetworkInfoSerializer
from res.resources.serializers import FlavorInfoSerializer
from res.resources.serializers import VmInfoSerializer
from res.resources.serializers import VnfInfoSerializer
from res.resources.serializers import VnfsInfoSerializer

logger = logging.getLogger(__name__)


class BaseService(object):

    def query_resources(self, res_type, logger, resources, cvt_fun, res_serializer):
        logger.debug("Enter query %s", res_type)

        resp = {
            'resp_data': [cvt_fun(res) for res in resources]
        }

        resp_serializer = res_serializer(data=resp)
        if not resp_serializer.is_valid():
            raise VNFRESException(resp_serializer.errors)

        return Response(
            data=resp,
            status=status.HTTP_200_OK
        )
