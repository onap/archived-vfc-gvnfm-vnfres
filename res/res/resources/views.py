# Copyright 2017 ZTE Corporation.
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

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from res.pub.utils.values import ignore_case_get
from res.pub.utils.syscomm import fun_name
from res.pub.database.models import NfInstModel

logger = logging.getLogger(__name__)


@api_view(http_method_names=['GET'])
def get_vnf(request, *args, **kwargs):
    vnf_inst_id = ignore_case_get(kwargs, "vnfInstanceId")
    logger.debug("[%s]vnf_inst_id=%s", fun_name(), vnf_inst_id)
    try:
        vnf_inst = NfInstModel.objects.filter(nfinstid=vnf_inst_id)
        if not vnf_inst:
            return Response(data={'error': 'Vnf(%s) does not exist' % vnf_inst_id}, 
                status=status.HTTP_404_NOT_FOUND)
        # TODO: fill resp_data
        resp_data = {"vnfInstanceId": vnf_inst_id}
        return Response(data=resp_data, status=status.HTTP_200_OK)
    except:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'Failed to get Vnf(%s)' % vnf_inst_id}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
