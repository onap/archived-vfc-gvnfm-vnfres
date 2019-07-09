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


def make_error_resp(status, detail):
    return Response(
        data={
            'status': status,
            'detail': detail
        },
        status=status
    )


def view_safe_call_with_log(logger):
    def view_safe_call(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except NotFoundException as e:
                logger.error(e.args[0])
                return make_error_resp(
                    detail=e.args[0],
                    status=status.HTTP_404_NOT_FOUND
                )
            except VNFRESException as e:
                logger.error(e.args[0])
                return make_error_resp(
                    detail=e.args[0],
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                logger.error(e.args[0])
                logger.error(traceback.format_exc())
                return make_error_resp(
                    detail='Unexpected exception',
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return wrapper
    return view_safe_call


def query_resources(res_type, logger, resources, cvt_fun, res_serializer):
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


class getVnf(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: VnfInfoSerializer(),
            status.HTTP_404_NOT_FOUND: 'Vnf does not exist',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request, vnfInstanceId):
        logger.debug("[%s]vnf_inst_id=%s", fun_name(), vnfInstanceId)

        vnf_inst = NfInstModel.objects.filter(nfinstid=vnfInstanceId)
        if not vnf_inst:
            raise NotFoundException('Vnf(%s) does not exist' % vnfInstanceId)

        resp_data = fill_resp_data(vnf_inst[0])

        vnf_info_serializer = VnfInfoSerializer(data=resp_data)
        if not vnf_info_serializer.is_valid():
            raise VNFRESException(vnf_info_serializer.errors)

        return Response(
            data=resp_data,
            status=status.HTTP_200_OK
        )


def fill_resp_data(vnf):
    logger.info('Get the StorageInstModel of list')
    storage_inst = StorageInstModel.objects.filter(instid=vnf.nfinstid)
    arr = []
    for s in storage_inst:
        storage = {
            "virtualStorageInstanceId": s.storageid,
            "virtualStorageDescId": s.storagetype,
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
    logger.info('Get the VimInstModel of list.')
    vms = VmInstModel.objects.filter(instid=vnf.nfinstid)
    vm_arr = []
    for vm in vms:
        vm_dic = {
            "vmid": vm.vmid,
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
            "nodeId": vm.nodeId
        }
        vm_arr.append(vm_dic)

    resp_data = {
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
            "vmInfo": vm_arr,
            "vnfcResourceInfo": vnfc_arr,
            "virtualLinkResourceInfo": vl_arr,
            "virtualStorageResourceInfo": arr
        },
        "metadata": vnf.input_params,
        "extensions": vnf.vnfd_model
    }
    return resp_data


class getVnfs(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: VnfsInfoSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request):
        return query_resources(
            res_type="Vnfs",
            logger=logger,
            resources=NfInstModel.objects.all(),
            cvt_fun=fill_resp_data,
            res_serializer=VnfsInfoSerializer
        )


class getVms(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: VmInfoSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request, vnfInstanceId):
        return query_resources(
            res_type="Vms",
            logger=logger,
            resources=VmInstModel.objects.filter(instid=vnfInstanceId),
            cvt_fun=fill_vms_data,
            res_serializer=VmInfoSerializer
        )


def fill_vms_data(vm):
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


class getFlavors(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: FlavorInfoSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request, vnfInstanceId):
        return query_resources(
            res_type="Flavors",
            logger=logger,
            resources=FlavourInstModel.objects.filter(instid=vnfInstanceId),
            cvt_fun=fill_flavours_data,
            res_serializer=FlavorInfoSerializer
        )


def fill_flavours_data(f):
    flavours_data = {
        "flavourid": f.flavourid,
        "name": f.name,
        "vcpu": f.vcpu,
        "memory": f.memory,
        "extraspecs": f.extraspecs,
        "instid": f.instid,
        "tenant": f.tenant,
        "vimid": f.vimid,
        "resouceid": f.resouceid,
        "create_time": f.create_time
    }
    return flavours_data


class getNetworks(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: NetworkInfoSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request, vnfInstanceId):
        return query_resources(
            res_type="Networks",
            logger=logger,
            resources=NetworkInstModel.objects.filter(instid=vnfInstanceId),
            cvt_fun=fill_networks_data,
            res_serializer=NetworkInfoSerializer
        )


def fill_networks_data(network):
    networks_data = {
        "networkid": network.networkid,
        "vimid": network.vimid,
        "resouceid": network.resouceid,
        "insttype": network.insttype,
        "instid": network.instid,
        "name": network.name
    }
    return networks_data


class getSubnets(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: SubnetInfoSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request, vnfInstanceId):
        return query_resources(
            res_type="Subnets",
            logger=logger,
            resources=SubNetworkInstModel.objects.filter(instid=vnfInstanceId),
            cvt_fun=fill_subnets_data,
            res_serializer=SubnetInfoSerializer
        )


def fill_subnets_data(subnet):
    subnets_data = {
        "subnetworkid": subnet.subnetworkid,
        "vimid": subnet.vimid,
        "resouceid": subnet.resouceid,
        "networkid": subnet.networkid,
        "insttype": subnet.insttype,
        "instid": subnet.instid,
        "name": subnet.name,
        "cidr": subnet.cidr
    }
    return subnets_data


class getCps(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CpsInfoSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request, vnfInstanceId):
        return query_resources(
            res_type="Cps",
            logger=logger,
            resources=CPInstModel.objects.filter(ownerid=vnfInstanceId),
            cvt_fun=fill_cps_data,
            res_serializer=CpsInfoSerializer
        )


def fill_cps_data(cp):
    cps_data = {
        "cpinstanceid": cp.cpinstanceid,
        "cpdid": cp.cpdid,
        "cpinstancename": cp.cpinstancename,
        "vlinstanceid": cp.vlinstanceid,
        "ownertype": cp.ownertype,
        "ownerid": cp.ownerid,
        "relatedtype": cp.relatedtype
    }
    return cps_data


class getVolumes(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: VolumeInfoSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request, vnfInstanceId):
        return query_resources(
            res_type="Volumes",
            logger=logger,
            resources=StorageInstModel.objects.filter(instid=vnfInstanceId),
            cvt_fun=fill_volumes_data,
            res_serializer=VolumeInfoSerializer
        )


def fill_volumes_data(v):
    volumes_data = {
        "storageid": v.storageid,
        "vimid": v.vimid,
        "resouceid": v.resouceid,
        "insttype": v.insttype,
        "instid": v.instid,
        "storagetype": v.storagetype,
        "size": v.size
    }
    return volumes_data
