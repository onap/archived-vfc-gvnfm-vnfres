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

from res.biz.base import BaseService
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
from res.resources.serializers import SubnetInfoSerializer
from res.resources.serializers import NetworkInfoSerializer
from res.resources.serializers import FlavorInfoSerializer
from res.resources.serializers import VmInfoSerializer
from res.resources.serializers import VnfInfoSerializer
from res.resources.serializers import VnfsInfoSerializer

logger = logging.getLogger(__name__)


class GetVnfsService(BaseService):

    def __init__(self):
        super(GetVnfsService, self).__init__()

    def get_vnfs(self):
        return self.query_resources(
            res_type="Vnfs",
            logger=logger,
            resources=NfInstModel.objects.all(),
            cvt_fun=self._fill_resp_data,
            res_serializer=VnfsInfoSerializer
        )

    def get_vnf(self, vnf_instance_id):
        vnf = NfInstModel.objects.filter(nfinstid=vnf_instance_id)
        if not vnf:
            raise NotFoundException('Vnf(%s) does not exist' % vnf_instance_id)

        return self._fill_resp_data(vnf[0])

    def _fill_resp_data(self, vnf):
        def make_virtual_storage_resource():
            logger.info('Get the StorageInstModel of list')
            return [{"virtualStorageInstanceId": s.storageid,
                     "virtualStorageDescId": s.storagetype,
                     "storageResource": {
                         "vimId": s.vimid,
                         "resourceId": s.resouceid
                     }}
                    for s in StorageInstModel.objects.filter(instid=vnf.nfinstid)]

        def make_virtual_link_resource():
            logger.info('Get the VLInstModel of list.')
            vl_inst = VLInstModel.objects.filter(ownerid=vnf.nfinstid)
            vl_arr = []
            for v in vl_inst:
                net = NetworkInstModel.objects.filter(networkid=v.relatednetworkid)
                if not net:
                    raise VNFRESException(
                        'NetworkInst(%s) does not exist.' %
                        v.relatednetworkid)
                v_dic = {
                    "virtualLinkInstanceId": v.vlinstanceid,
                    "virtualLinkDescId": v.vldid,
                    "networkResource": {
                        "vimId": net[0].vimid,
                        "resourceId": net[0].resouceid
                    }
                }
                vl_arr.append(v_dic)
            return vl_arr

        def make_vnfc_resource():
            logger.info('Get VNFCInstModel of list.')
            vnfc_insts = VNFCInstModel.objects.filter(instid=vnf.nfinstid)
            vnfc_arr = []
            for vnfc in vnfc_insts:
                vm = VmInstModel.objects.filter(vmid=vnfc.vmid)
                if not vm:
                    raise VNFRESException('VmInst(%s) does not exist.' % vnfc.vmid)
                storage = StorageInstModel.objects.filter(ownerid=vm[0].vmid)
                if not storage:
                    raise VNFRESException(
                        'StorageInst(%s) does not exist.' %
                        vm[0].vmid)
                vnfc_dic = {
                    "vnfcInstanceId": vnfc.vnfcinstanceid,
                    "vduId": vnfc.vduid,
                    "computeResource": {
                        "vimId": vm[0].vimid,
                        "resourceId": vm[0].resouceid
                    },
                    "storageResourceIds": [s.storageid for s in storage]
                }
                vnfc_arr.append(vnfc_dic)
            return vnfc_arr

        def make_vm():
            logger.info('Get the VimInstModel of list.')
            return [{"vmid": vm.vmid,
                     "vimid": vm.vimid,
                     "tenant": vm.tenant,
                     "resouceid": vm.resouceid,
                     "vmname": vm.vmname,
                     "nic_array": vm.nic_array,
                     "metadata": vm.metadata,
                     "volume_array": vm.volume_array,
                     "server_group": vm.server_group,
                     "availability_zone": vm.availability_zone,
                     "flavor_id": vm.flavor_id,
                     "security_groups": vm.security_groups,
                     "operationalstate": vm.operationalstate,
                     "insttype": vm.insttype,
                     "is_predefined": vm.is_predefined,
                     "create_time": vm.create_time,
                     "instid": vm.instid,
                     "nodeId": vm.nodeId}
                    for vm in VmInstModel.objects.filter(instid=vnf.nfinstid)]


        virtual_storage_resources = make_virtual_storage_resource()
        virtual_link_resource = make_virtual_link_resource()
        vnfc_resource = make_vnfc_resource()
        vm_info = make_vm()
        return {
            "vnfInstanceId": vnf.nfinstid,
            "vnfInstanceName": vnf.nf_name,
            "vnfInstanceDescription": vnf.nf_desc,
            "onboardedVnfPkgInfoId": vnf.package_id,
            "vnfdId": vnf.vnfdid,
            "vnfdVersion": vnf.version,
            "vnfSoftwareVersion": vnf.vnfSoftwareVersion,
            "vnfProvider": vnf.vendor,
            "vnfProductName": vnf.netype,
            "vnfConfigurableProperties": vnf.vnfConfigurableProperties,
            "instantiationState": vnf.status,
            "instantiatedVnfInfo": {
                "flavourId": vnf.flavour_id,
                "vnfState": vnf.status,
                "scaleStatus": [],
                "extCpInfo": [],
                "extVirtualLink": [],
                "monitoringParameters": {},
                "localizationLanguage": vnf.localizationLanguage,
                "vmInfo": vm_info,
                "vnfcResourceInfo": vnfc_resource,
                "virtualLinkResourceInfo": virtual_link_resource,
                "virtualStorageResourceInfo": virtual_storage_resources
            },
            "metadata": vnf.input_params,
            "extensions": vnf.vnfd_model
        }
