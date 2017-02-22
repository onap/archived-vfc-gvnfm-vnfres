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

from res.pub.exceptions import VNFRESException
from res.pub.utils.values import ignore_case_get
from res.pub.utils.syscomm import fun_name
from res.pub.database.models import NfInstModel, CPInstModel, StorageInstModel, NetworkInstModel, VLInstModel, \
    VNFCInstModel, VmInstModel, VimModel, VimUserModel

logger = logging.getLogger(__name__)


@api_view(http_method_names=['GET'])
def get_vnf(request, *args, **kwargs):
    vnf_inst_id = ignore_case_get(kwargs, "vnfInstanceId")
    logger.debug("[%s]vnf_inst_id=%s", fun_name(), vnf_inst_id)
    try:
        vnf_inst = NfInstModel.objects.filter(nfinstid=vnf_inst_id)
        if not vnf_inst:
            return Response(data={'error': 'Vnf(%s) does not exist' % vnf_inst_id}, status=status.HTTP_404_NOT_FOUND)
        # TODO: fill resp_data
        # resp_data = {"vnfInstanceId": vnf_inst_id, "vnfInstanceName": vnf_inst[0].nf_name, "vnfInstanceDescription":}
        resp_data = fill_resp_data(vnf_inst[0])
        return Response(data=resp_data, status=status.HTTP_200_OK)
    except:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'Failed to get Vnf(%s)' % vnf_inst_id}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def fill_resp_data(vnf):
    # cp_insts = CPInstModel.objects.filter(ownerid=vnf_inst_id)
    # if not cp_insts:
    #     raise VNFRESException('CpInst(%s) does not exist.' % vnf_inst_id)
    # cp_inst = cp_insts.first()
    logger.info('Get the StorageInstModel of list')
    storage_inst = StorageInstModel.objects.filter(instid=vnf.nfinstid)
    arr = []
    for s in storage_inst:
        storage = {
            "virtualStorageInstanceId": s.storageid,
            "virtualStorageDescId": s.storageDesc,
            "storageResource": {
                "vimId": s.vimid,
                "resourceId": s.resouceid
            }
        }
        arr.append(storage)
    logger.info('Get the VLInstModel of list.')
    vl_inst = VLInstModel.objects.filter(ownerid=vnf.nfinstid)
    vl_arr = []
    for v in vl_inst:
        net = NetworkInstModel.objects.filter(networkid=v.relatednetworkid)
        if not net:
            raise VNFRESException('NetworkInst(%s) does not exist.' % v.relatednetworkid)
        v_dic = {
                    "virtualLinkInstanceId": v.vlinstanceid,
                    "virtualLinkDescId": v.vldid,
                    "networkResource": {
                        "vimId": net[0].vimid,
                        "resourceId": net[0].resouceid
                    }
                }
        vl_arr.append(v_dic)
    logger.info('Get VNFCInstModel of list.')
    vnfc_insts = VNFCInstModel.objects.filter(nfinstid=vnf.nfinstid)
    vnfc_arr = []
    for vnfc in vnfc_insts:
        vm = VmInstModel.objects.filter(vmid=vnfc.vmid)
        if not vm:
            raise VNFRESException('VmInst(%s) does not exist.' % vnfc.vmid)
        storage = StorageInstModel.objects.filter(ownerid=vm[0].vmid)
        if not storage:
            raise VNFRESException('StorageInst(%s) does not exist.' % vm[0].vmid)
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
    logger.info('Get the VimInstModel of list.')
    vms = VmInstModel.objects.filter(instid=vnf.nfinstid)
    vim_arr = []
    # The 'vimInfoId' and 'vimId' each value are same
    for vm in vms:
        vims = VimModel.objects.filter(vimid=vm.vimid)
        for vim in vims:
            vim_users = VimUserModel.objects.filter(vimid=vim.vimid)
            vim_dic = {
                    "vimInfoId": vim.vimid,
                    "vimId": vim.vimid,
                    "interfaceInfo": {
                        "vimType": vim.type,
                        "apiVersion": vim.version,
                        "protocolType": (vim.apiurl.split(':')[0] if vim.apiurl and vim.apiurl.index(':') else 'http')
                    },
                    "accessInfo": {
                        "tenant": (vim_users[0].defaulttenant if vim_users and vim_users[0].defaulttenant else ''),
                        "username": (vim_users[0].username if vim_users and vim_users[0].username else ''),
                        "password": (vim_users[0].password if vim_users and vim_users[0].password else '')
                    },
                    "interfaceEndpoint": vim.apiurl
            }
            vim_arr.append(vim_dic)

    resp_data = {
        "vnfInstanceId": vnf.nfinstid,
        "vnfInstanceName": vnf.nf_name,
        "vnfInstanceDescription": vnf.nf_desc,
        "onboardedVnfPkgInfoId": vnf.package_id,
        "vnfdId": vnf.vnfdid,
        "vnfdVersion": vnf.version,
        "vnfSoftwareVersion": vnf.vnfSoftwareVersion,
        "vnfProvider": vnf.vendor,
        "vnfProductName": vnf.producttype,
        "vnfConfigurableProperties": {vnf.vnfConfigurableProperties},
        "instantiationState": vnf.instantiationState,
        "instantiatedVnfInfo": {
            "flavourId": vnf.flavour_id,
            "vnfState": vnf.status,
            "scaleStatus": [],
            "extCpInfo": [],
            "extVirtualLink": [],
            "monitoringParameters": {},
            "localizationLanguage": vnf.localizationLanguage,
            "vimInfo": vim_arr,
            "vnfcResourceInfo": vnfc_arr,
            "virtualLinkResourceInfo": vl_arr,
            "virtualStorageResourceInfo": arr
        },
        "metadata": vnf.input_params,
        "extensions": vnf.extension
    }
    return resp_data


@api_view(http_method_names=['GET'])
def get_vnfs(request):
    logger.debug("Query all the vnfs[%s]", fun_name())
    try:
        vnf_insts = NfInstModel.objects.all()
        if not vnf_insts:
            return Response(data={'error': 'Vnfs does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # FIXME: fill resp_datas
        arr = []
        for vnf_inst in vnf_insts:
            arr.append(fill_resp_data(vnf_inst))
        return Response(data={'resp_data': arr}, status=status.HTTP_200_OK)
    except:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'Failed to get Vnfs'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)