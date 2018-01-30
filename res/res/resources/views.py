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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from res.pub.database.models import NfInstModel, StorageInstModel, NetworkInstModel, VLInstModel, \
    VNFCInstModel, VmInstModel, FlavourInstModel, SubNetworkInstModel, CPInstModel
from res.pub.exceptions import VNFRESException
from res.pub.utils.syscomm import fun_name
from res.resources.serializers import VolumeInfoSerializer, CpsInfoSerializer, SubnetInfoSerializer, \
    NetworkInfoSerializer, FlavorInfoSerializer, VmInfoSerializer, VnfInfoSerializer

logger = logging.getLogger(__name__)


class getVnfs(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: VnfInfoSerializer(),
            status.HTTP_404_NOT_FOUND: 'Vnf does not exist',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
    def get(self, request, vnfInstanceId):
        logger.debug("[%s]vnf_inst_id=%s", fun_name(), vnfInstanceId)
        try:
            vnf_inst = NfInstModel.objects.filter(nfinstid=vnfInstanceId)
            if not vnf_inst:
                return Response(data={'error': 'Vnf(%s) does not exist' % vnfInstanceId}, status=status.HTTP_404_NOT_FOUND)
            resp_data = fill_resp_data(vnf_inst[0])
            return Response(data=resp_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Failed to get Vnf(%s)' % vnfInstanceId}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    vnfc_insts = VNFCInstModel.objects.filter(instid=vnf.nfinstid)
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
    vm_arr = []
    # The 'vimInfoId' and 'vimId' each value are same
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


@api_view(http_method_names=['GET'])
def get_vnfs(request):
    logger.debug("Query all the vnfs[%s]", fun_name())
    try:
        vnf_insts = NfInstModel.objects.all()
        if not vnf_insts:
            return Response(data={'error': 'Vnfs does not exist'}, status=status.HTTP_404_NOT_FOUND)
        arr = []
        for vnf_inst in vnf_insts:
            arr.append(fill_resp_data(vnf_inst))
        return Response(data={'resp_data': arr}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(e.message)
        logger.error(traceback.format_exc())
        return Response(data={'error': 'Failed to get Vnfs'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class getVms(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: VmInfoSerializer(),
            status.HTTP_404_NOT_FOUND: 'Vms does not exist',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
    def get(self, request, vnfInstanceId):
        logger.debug("Query all the vms by vnfInstanceId[%s]", fun_name())
        try:
            vms = VmInstModel.objects.filter(instid=vnfInstanceId)
            if not vms:
                return Response(data={'error': 'Vms does not exist'}, status=status.HTTP_404_NOT_FOUND)
            arr = []
            for vm in vms:
                arr.append(fill_vms_data(vm))

            vmInfoSerializer = VmInfoSerializer(data={'resp_data': arr})
            isValid = vmInfoSerializer.is_valid()
            if not isValid:
                raise Exception(vmInfoSerializer.errors)

            return Response(data=vmInfoSerializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Failed to get Vms'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            status.HTTP_404_NOT_FOUND: 'Flavours does not exist',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
    def get(self, request, vnfInstanceId):
        logger.debug("Query all the flavors by vnfInstanceId[%s]", fun_name())
        try:
            flavours = FlavourInstModel.objects.filter(instid=vnfInstanceId)
            if not flavours:
                return Response(data={'error': 'Flavours does not exist'}, status=status.HTTP_404_NOT_FOUND)
            arr = []
            for flavour in flavours:
                arr.append(fill_flavours_data(flavour))

            flavorInfoSerializer = FlavorInfoSerializer(data={'resp_data': arr})
            isValid = flavorInfoSerializer.is_valid()
            if not isValid:
                raise Exception(flavorInfoSerializer.errors)

            return Response(data=flavorInfoSerializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Failed to get flavours'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            status.HTTP_404_NOT_FOUND: 'Networks does not exist',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
    def get(self, request, vnfInstanceId):
        logger.debug("Query all the networks by vnfInstanceId[%s]", fun_name())
        try:
            networks = NetworkInstModel.objects.filter(instid=vnfInstanceId)
            if not networks:
                return Response(data={'error': 'Networks does not exist'}, status=status.HTTP_404_NOT_FOUND)
            arr = []
            for network in networks:
                arr.append(fill_networks_data(network))

            networkInfoSerializer = NetworkInfoSerializer(data={'resp_data': arr})
            isValid = networkInfoSerializer.is_valid()
            if not isValid:
                raise Exception(networkInfoSerializer.errors)

            return Response(data=networkInfoSerializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Failed to get networks'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            status.HTTP_404_NOT_FOUND: 'Subnets does not exist',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
    def get(self, request, vnfInstanceId):
        logger.debug("Query all the subnets by vnfInstanceId[%s]", fun_name())
        try:
            subnets = SubNetworkInstModel.objects.filter(instid=vnfInstanceId)
            if not subnets:
                return Response(data={'error': 'Subnets does not exist'}, status=status.HTTP_404_NOT_FOUND)
            arr = []
            for subnet in subnets:
                arr.append(fill_subnets_data(subnet))
            subnetInfoSerializer = SubnetInfoSerializer(data={'resp_data': arr})
            isValid = subnetInfoSerializer.is_valid()
            if not isValid:
                raise Exception(subnetInfoSerializer.errors)

            return Response(data=subnetInfoSerializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Failed to get subnets'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            status.HTTP_404_NOT_FOUND: 'Cps does not exist',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
    def get(self, request, vnfInstanceId):
        logger.debug("Query all the cps by vnfInstanceId[%s]", fun_name())
        try:
            cps = CPInstModel.objects.filter(ownerid=vnfInstanceId)
            if not cps:
                return Response(data={'error': 'Cps does not exist'}, status=status.HTTP_404_NOT_FOUND)
            arr = []
            for cp in cps:
                arr.append(fill_cps_data(cp))
            cpInfoSerializer = CpsInfoSerializer(data={'resp_data': arr})
            isValid = cpInfoSerializer.is_valid()
            if not isValid:
                raise Exception(cpInfoSerializer.errors)

            return Response(data=cpInfoSerializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Failed to get cps'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            status.HTTP_404_NOT_FOUND: 'Volumes does not exist',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
    def get(self, request, vnfInstanceId):
        logger.debug("Query all the volumes by vnfInstanceId[%s]", fun_name())
        try:
            volumes = StorageInstModel.objects.filter(instid=vnfInstanceId)
            if not volumes:
                return Response(data={'error': 'Volumes does not exist'}, status=status.HTTP_404_NOT_FOUND)
            arr = []
            for v in volumes:
                arr.append(fill_volumes_data(v))
            volumeSerializer = VolumeInfoSerializer(data={'resp_data': arr})
            isValid = volumeSerializer.is_valid()
            if not isValid:
                raise Exception(volumeSerializer.errors)

            return Response(data=volumeSerializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Failed to get volumes'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
