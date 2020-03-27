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

from res.biz.base import BaseService
from res.pub.database.models import NetworkInstModel
from res.resources.serializers import NetworkInfoSerializer

logger = logging.getLogger(__name__)


class GetNetworksService(BaseService):

    def __init__(self):
        super(GetNetworksService, self).__init__()

    def get_networks(self, vnf_instance_id):
        return self.query_resources(
            res_type="Networks",
            logger=logger,
            resources=NetworkInstModel.objects.filter(instid=vnf_instance_id),
            cvt_fun=self.fill_networks_data,
            res_serializer=NetworkInfoSerializer
        )

    def fill_networks_data(self, network):
        networks_data = {
            "networkid": network.networkid,
            "vimid": network.vimid,
            "resouceid": network.resouceid,
            "insttype": network.insttype,
            "instid": network.instid,
            "name": network.name
        }
        return networks_data
