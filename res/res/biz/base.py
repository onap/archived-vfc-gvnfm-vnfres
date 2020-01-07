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

from res.pub.exceptions import VNFRESException

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
