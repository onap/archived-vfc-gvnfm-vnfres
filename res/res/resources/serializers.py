# Copyright 2018 ZTE Corporation.
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

from rest_framework import serializers


class StorageResourceSerializer(serializers.Serializer):
    resourceId = serializers.CharField(help_text="resourceId", required=True)
    vimId = serializers.CharField(help_text="vimId", required=True)


class virtualStorageResourceInfoSerializer(serializers.Serializer):
    virtualStorageInstanceId = serializers.CharField(help_text="virtualStorageInstanceId", required=True)
    virtualStorageDescId = serializers.CharField(help_text="virtualStorageDescId", required=True, allow_null=True)
    storageResource = StorageResourceSerializer(help_text="storageResource", required=True)


class virtualLinkResourceInfoSerializer(serializers.Serializer):
    pass


class vnfcResourceInfoSerializer(serializers.Serializer):
    pass


class accessInfoSerializer(serializers.Serializer):
    tenant = serializers.CharField(help_text="tenant", required=True)
    username = serializers.CharField(help_text="username", required=True)
    password = serializers.CharField(help_text="password", required=True)


class InterfaceInfoSerializer(serializers.Serializer):
    vimType = serializers.CharField(help_text="vimType", required=True)
    apiVersion = serializers.CharField(help_text="apiVersion", required=True)
    protocolType = serializers.ChoiceField(help_text="protocolType", choices=['http', 'https'], required=True)


class VmResponseSerializer(serializers.Serializer):
    vmid = serializers.CharField(help_text="vmid", required=True)
    vimid = serializers.CharField(help_text="the vim id", required=True)
    resouceid = serializers.CharField(help_text="the resouce id", required=True)
    tenant = serializers.CharField(help_text="tenant", required=True, allow_null=True)
    instid = serializers.CharField(help_text="the inst id", required=True)
    vmname = serializers.CharField(help_text="vmname", required=True)
    insttype = serializers.IntegerField(help_text="insttype", required=True)
    operationalstate = serializers.CharField(help_text="operationalstate", required=True, allow_null=True)
    is_predefined = serializers.IntegerField(help_text="is_predefined", required=True)
    security_groups = serializers.CharField(help_text="security_groups", required=True)
    flavor_id = serializers.CharField(help_text="flavor_id", required=True)
    availability_zone = serializers.CharField(help_text="availability_zone", required=True)
    server_group = serializers.CharField(help_text="server_group", required=True)
    volume_array = serializers.CharField(help_text="volume_array", required=True)
    metadata = serializers.CharField(help_text="metadata", required=True)
    nic_array = serializers.CharField(help_text="nic_array", required=True)


class vimInfoSerializer(serializers.Serializer):
    vimInfoId = serializers.CharField(help_text="vimInfoId", required=False, allow_null=True)
    vimId = serializers.CharField(help_text="vimId", required=False, allow_null=True)
    interfaceEndpoint = serializers.CharField(help_text="interfaceEndpoint", required=False, allow_null=True)
    interfaceInfo = InterfaceInfoSerializer(help_text="vimInfoId", required=False, allow_null=True)
    accessInfo = accessInfoSerializer(help_text="accessInfo", required=False, allow_null=True)


class monitoringParametersSerializer(serializers.Serializer):
    pass


class linkPortsSerializer(serializers.Serializer):
    resourceId = serializers.CharField(help_text="resourceId", required=True)
    vimId = serializers.CharField(help_text="vimId", required=False)


class resourceHandleSerializer(serializers.Serializer):
    resourceId = serializers.CharField(help_text="resourceId", required=True)
    vimId = serializers.CharField(help_text="vimId", required=False)
    resourceProviderId = serializers.CharField(help_text="resourceProviderId", required=False)


class ExtVirtualLinkInfoSerializer(serializers.Serializer):
    extVirtualLinkId = serializers.CharField(help_text="extVirtualLinkId", required=True)
    resourceHandle = resourceHandleSerializer(help_text="iPAddress", required=True)
    linkPorts = linkPortsSerializer(help_text="iPAddress", many=True, allow_null=True)


class l3AddressDataSerializer(serializers.Serializer):
    iPAddressType = serializers.ChoiceField(help_text="iPAddressType", choices=['IPv4', 'IPv6'], required=True)
    iPAddress = serializers.CharField(help_text="iPAddress", required=True)


class NetworkAddressSerializer(serializers.Serializer):
    addressType = serializers.ChoiceField(help_text="addressType", choices=['MAC', 'IP'], required=True)
    l2AddressData = serializers.CharField(help_text="l2AddressData", required=False)
    l3AddressData = l3AddressDataSerializer(help_text="addresses", required=False)


class extCpInfoSerializer(serializers.Serializer):
    cpInstanceId = serializers.CharField(help_text="cpInstanceId", required=False, allow_null=True)
    cpdId = serializers.IntegerField(help_text="cpdId", required=True)
    numDynamicAddresses = serializers.IntegerField(help_text="numDynamicAddresses", required=False, allow_null=True)
    addresses = NetworkAddressSerializer(help_text="addresses", many=True, allow_null=True)


class ScaleInfoSerializer(serializers.Serializer):
    aspectId = serializers.CharField(help_text="aspectId", required=True, allow_null=True)
    scaleLevel = serializers.IntegerField(help_text="scaleLevel", required=True, allow_null=True)


class instantiatedVnfInfoSerializer(serializers.Serializer):
    flavourId = serializers.CharField(help_text="flavour Id", required=True, allow_null=True)
    vnfState = serializers.ChoiceField(help_text="vnf State", choices=['STARTED', 'STOPPED'], required=True, allow_null=True)
    localizationLanguage = serializers.CharField(help_text="localizationLanguage", required=True, allow_null=True)
    metadata = serializers.CharField(help_text="metadata", required=True, allow_null=True)
    extensions = serializers.CharField(help_text="extensions", required=True, allow_null=True)
    scaleStatus = ScaleInfoSerializer(help_text="scaleStatus", many=True)
    extCpInfo = extCpInfoSerializer(help_text="extCpInfo", many=True)
    extVirtualLink = ExtVirtualLinkInfoSerializer(help_text="extVirtualLink", many=True)
    monitoringParameters = monitoringParametersSerializer(help_text="monitoringParameters", allow_null=True)
    vmInfo = VmResponseSerializer(help_text="vmInfo", many=True, allow_null=True)
    vimInfo = vimInfoSerializer(help_text="vimInfo", many=True, allow_null=True)
    vnfcResourceInfo = vnfcResourceInfoSerializer(help_text="vnfcResourceInfo", many=True)
    virtualLinkResourceInfo = virtualLinkResourceInfoSerializer(help_text="virtualLinkResourceInfo", many=True)
    virtualStorageResourceInfo = virtualStorageResourceInfoSerializer(help_text="virtualStorageResourceInfo", many=True)


class VnfInfoSerializer(serializers.Serializer):
    vnfInstanceId = serializers.CharField(help_text="vnf Instance Id", required=True)
    vnfInstanceName = serializers.CharField(help_text="vnf Instance Name", required=True)
    vnfInstanceDescription = serializers.CharField(help_text="vnfInstanceDescription", required=True, allow_null=True)
    onboardedVnfPkgInfoId = serializers.CharField(help_text="onboarded Vnf Pkg Info Id", required=False,
                                                  allow_null=True)
    vnfdId = serializers.CharField(help_text="vnfdId", required=True, allow_null=True)
    vnfdVersion = serializers.CharField(help_text="vnfd Version", required=False, allow_null=True)
    vnfSoftwareVersion = serializers.CharField(help_text="vnfSoftwareVersion", required=True, allow_null=True)
    vnfProvider = serializers.CharField(help_text="vnf Provider", required=False, allow_null=True)
    vnfProductName = serializers.CharField(help_text="vnfProductName", required=False, allow_null=True)
    vnfConfigurableProperties = serializers.CharField(help_text="vnfConfigurableProperties", required=False, allow_null=True)
    instantiationState = serializers.CharField(help_text="instantiationState", required=False, allow_null=True)
    instantiatedVnfInfo = instantiatedVnfInfoSerializer(help_text="instantiatedVnfInfo", required=True)


class VmInfoSerializer(serializers.Serializer):
    resp_data = VmResponseSerializer(help_text="the response data", many=True)


class FlavorResponseSerializer(serializers.Serializer):
    flavourid = serializers.CharField(help_text="flavourid", required=True)
    vimid = serializers.CharField(help_text="the vim id", required=True)
    resouceid = serializers.CharField(help_text="the resouce id", required=True)
    tenant = serializers.CharField(help_text="tenant", required=True, allow_null=True)
    instid = serializers.CharField(help_text="the inst id", required=True)
    name = serializers.CharField(help_text="name", required=True)
    extraspecs = serializers.CharField(help_text="extraspecs", required=True)
    create_time = serializers.CharField(help_text="create_time", required=True, allow_null=True)
    memory = serializers.IntegerField(help_text="memory", required=True)
    vcpu = serializers.IntegerField(help_text="vcpu", required=True)


class FlavorInfoSerializer(serializers.Serializer):
    resp_data = FlavorResponseSerializer(help_text="the response data", many=True)


class NetworkResponseSerializer(serializers.Serializer):
    networkid = serializers.CharField(help_text="networkid", required=True)
    vimid = serializers.CharField(help_text="the vim id", required=True)
    resouceid = serializers.CharField(help_text="the resouce id", required=True)
    insttype = serializers.IntegerField(help_text="the inst type", required=True)
    instid = serializers.CharField(help_text="the inst id", required=True)
    name = serializers.CharField(help_text="name", required=True)


class NetworkInfoSerializer(serializers.Serializer):
    resp_data = NetworkResponseSerializer(help_text="the response data", many=True)


class SubnetResponseSerializer(serializers.Serializer):
    subnetworkid = serializers.CharField(help_text="the subnetwork id", required=True)
    vimid = serializers.CharField(help_text="the vim id", required=True)
    resouceid = serializers.CharField(help_text="the resouce id", required=True)
    networkid = serializers.CharField(help_text="the network id", required=True)
    insttype = serializers.IntegerField(help_text="the inst type", required=True)
    instid = serializers.CharField(help_text="the inst id", required=True)
    name = serializers.CharField(help_text="name", required=True)
    cidr = serializers.CharField(help_text="cidr", required=True)


class SubnetInfoSerializer(serializers.Serializer):
    resp_data = SubnetResponseSerializer(help_text="the response data", many=True)


class CpResponseSerializer(serializers.Serializer):
    cpinstanceid = serializers.CharField(help_text="the cp instance id", required=True)
    cpdid = serializers.CharField(help_text="the cpd id", required=True)
    cpinstancename = serializers.CharField(help_text="the cp instance name of vnf", required=True)
    vlinstanceid = serializers.CharField(help_text="the vl instance id of vnf", required=True)
    ownertype = serializers.IntegerField(help_text="the owner type of vnf", required=True)
    ownerid = serializers.CharField(help_text="the owner id of vnf", required=True)
    relatedtype = serializers.IntegerField(help_text="the related type", required=True)


class CpsInfoSerializer(serializers.Serializer):
    resp_data = CpResponseSerializer(help_text="the response data", many=True)


class VolumeResponseSerializer(serializers.Serializer):
    storageid = serializers.CharField(help_text="the storage id", required=True)
    vimid = serializers.CharField(help_text="the vim id", required=True)
    resouceid = serializers.CharField(help_text="the resouce id of vnf", required=True)
    insttype = serializers.IntegerField(help_text="the inst type of vnf", required=True)
    instid = serializers.CharField(help_text="the inst id of vnf", required=True)
    storagetype = serializers.CharField(help_text="the storage type of vnf", required=True)
    size = serializers.CharField(help_text="the size of storage", required=True)


class VolumeInfoSerializer(serializers.Serializer):
    resp_data = VolumeResponseSerializer(help_text="the response data", many=True)
