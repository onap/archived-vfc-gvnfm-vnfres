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
from res.pub.database.models import FlavourInstModel
from res.resources.serializers import FlavorInfoSerializer

logger = logging.getLogger(__name__)


class GetFlavorsService(BaseService):

    def __init__(self):
        super(GetFlavorsService, self).__init__()

    def get_flavors(self, vnf_instance_id):
        return self.query_resources(
            res_type="Flavors",
            logger=logger,
            resources=FlavourInstModel.objects.filter(
                instid=vnf_instance_id),
            cvt_fun=self.fill_flavours_data,
            res_serializer=FlavorInfoSerializer
        )

    def fill_flavours_data(self, flavor):
        flavours_data = {
            "flavourid": flavor.flavourid,
            "name": flavor.name,
            "vcpu": flavor.vcpu,
            "memory": flavor.memory,
            "extraspecs": flavor.extraspecs,
            "instid": flavor.instid,
            "tenant": flavor.tenant,
            "vimid": flavor.vimid,
            "resouceid": flavor.resouceid,
            "create_time": flavor.create_time
        }
        return flavours_data
