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
from res.pub.database.models import VmInstModel
from res.resources.serializers import VmInfoSerializer

logger = logging.getLogger(__name__)


class GetVmsService(BaseService):

    def __init__(self):
        super(GetVmsService, self).__init__()

    def get_vms(self, vnf_instance_id):
        return self.query_resources(
            res_type="Vms",
            logger=logger,
            resources=VmInstModel.objects.filter(instid=vnf_instance_id),
            cvt_fun=self.fill_vms_data,
            res_serializer=VmInfoSerializer
        )

    def fill_vms_data(self, vm):
        vms_data = {
            "vmid": vm.vmid,
            "vimid": vm.vimid,
            "resouceid": vm.resouceid,
            "insttype": vm.insttype,
            "instid": vm.instid,
            "vmname": vm.vmname,
            "operationalstate": vm.operationalstate,
            "tenant": vm.tenant,
            "is_predefined": vm.is_predefined,
            "security_groups": vm.security_groups,
            "flavor_id": vm.flavor_id,
            "availability_zone": vm.availability_zone,
            "server_group": vm.server_group,
            "volume_array": vm.volume_array,
            "metadata": vm.metadata,
            "nic_array": vm.nic_array
        }
        return vms_data
