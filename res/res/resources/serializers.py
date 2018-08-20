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


class ResourceSerializer(serializers.Serializer):
    resourceId = serializers.CharField(
        help_text="ID of resource",
        required=True,
        max_length=255,
        allow_null=True)
    vimId = serializers.CharField(
        help_text="ID of VIM",
        required=True,
        max_length=255,
        allow_null=True)


class VirtualStorageResourceInfoSerializer(serializers.Serializer):
    virtualStorageInstanceId = serializers.CharField(
        help_text="ID of virtual storage instance",
        required=False,
        max_length=255,
        allow_null=True)
    virtualStorageDescId = serializers.CharField(
        help_text="Description ID of virtual storage",
        required=False,
        max_length=255,
        allow_null=True)
    storageResource = ResourceSerializer(
        help_text="Storage resource",
        required=False,
        allow_null=True)


class VirtualLinkResourceInfoSerializer(serializers.Serializer):
    virtualLinkInstanceId = serializers.CharField(
        help_text="ID of virtual link instance",
        required=False,
        max_length=255,
        allow_null=True)
    virtualLinkDescId = serializers.CharField(
        help_text="Description ID of virtual link",
        required=False,
        max_length=255,
        allow_null=True)
    networkResource = ResourceSerializer(
        help_text="Network resource",
        required=False,
        allow_null=True)


class VnfcResourceInfoSerializer(serializers.Serializer):
    vnfcInstanceId = serializers.CharField(
        help_text="ID of vnfc instance",
        required=False,
        max_length=255,
        allow_null=True)
    vduId = serializers.CharField(
        help_text="Id of virtual data unit",
        required=False,
        max_length=255,
        allow_null=True)
    storageResourceIds = serializers.CharField(
        help_text="ID list of storage resources",
        required=False,
        max_length=255,
        allow_null=True)
    computeResource = ResourceSerializer(
        help_text="Compute resource",
        required=False,
        allow_null=True)


class AccessInfoSerializer(serializers.Serializer):
    tenant = serializers.CharField(
        help_text="Tenant",
        required=False,
        max_length=255,
        allow_null=True)
    username = serializers.CharField(
        help_text="User Name",
        required=False,
        max_length=255,
        allow_null=True)
    password = serializers.CharField(
        help_text="Password",
        required=False,
        max_length=255,
        allow_null=True)


class InterfaceInfoSerializer(serializers.Serializer):
    vimType = serializers.CharField(
        help_text="VIM type",
        required=False,
        max_length=255,
        allow_null=True)
    apiVersion = serializers.CharField(
        help_text="API version",
        required=False,
        max_length=255,
        allow_null=True)
    protocolType = serializers.ChoiceField(
        help_text="Protocol type",
        choices=['http', 'https'],
        required=False,
        allow_null=True)


class VmResponseSerializer(serializers.Serializer):
    vmid = serializers.CharField(
        help_text="ID of VM",
        required=True,
        max_length=255,
        allow_null=True)
    vimid = serializers.CharField(
        help_text="ID of VIM",
        required=True,
        max_length=255,
        allow_null=True)
    resouceid = serializers.CharField(
        help_text="ID of resource",
        required=True,
        max_length=255,
        allow_null=True)
    tenant = serializers.CharField(
        help_text="Tenant",
        required=True,
        max_length=255,
        allow_null=True)
    instid = serializers.CharField(
        help_text="ID of instance",
        required=True,
        max_length=255,
        allow_null=True)
    vmname = serializers.CharField(
        help_text="Name of VM",
        required=True,
        max_length=255,
        allow_null=True)
    insttype = serializers.IntegerField(
        help_text="Instance type",
        required=True,
        allow_null=True)
    operationalstate = serializers.CharField(
        help_text="Operational state",
        required=True,
        max_length=255,
        allow_null=True)
    is_predefined = serializers.IntegerField(
        help_text="Is predefined",
        required=True,
        allow_null=True)
    security_groups = serializers.CharField(
        help_text="Security groups",
        required=True,
        max_length=255,
        allow_null=True)
    flavor_id = serializers.CharField(
        help_text="ID of flavor",
        required=True,
        max_length=255,
        allow_null=True)
    availability_zone = serializers.CharField(
        help_text="Availability zone",
        required=True,
        max_length=255,
        allow_null=True)
    server_group = serializers.CharField(
        help_text="Server group",
        required=True,
        max_length=255,
        allow_null=True)
    volume_array = serializers.CharField(
        help_text="Volume array",
        required=True,
        max_length=255,
        allow_null=True)
    metadata = serializers.CharField(
        help_text="Metadata",
        required=True,
        max_length=255,
        allow_null=True)
    nic_array = serializers.CharField(
        help_text="Nic array",
        required=True,
        max_length=255,
        allow_null=True)
    create_time = serializers.CharField(
        help_text="Create time",
        required=False,
        max_length=255,
        allow_null=True)
    nodeId = serializers.CharField(
        help_text="ID of node",
        required=False,
        max_length=255,
        allow_null=True)


class VimInfoSerializer(serializers.Serializer):
    vimInfoId = serializers.CharField(
        help_text="ID of VIM info",
        required=False,
        max_length=255,
        allow_null=True)
    vimId = serializers.CharField(
        help_text="ID of VIM",
        required=False,
        max_length=255,
        allow_null=True)
    interfaceEndpoint = serializers.CharField(
        help_text="Interface endpoint",
        required=False,
        max_length=255,
        allow_null=True)
    interfaceInfo = InterfaceInfoSerializer(
        help_text="ID of VIM info",
        required=False,
        allow_null=True)
    accessInfo = AccessInfoSerializer(
        help_text="Access info",
        required=False,
        allow_null=True)


class LinkPortsSerializer(serializers.Serializer):
    resourceId = serializers.CharField(
        help_text="ID of resource",
        required=True,
        max_length=255,
        allow_null=True)
    vimId = serializers.CharField(
        help_text="ID of VIM",
        required=False,
        max_length=255,
        allow_null=True)


class ResourceHandleSerializer(serializers.Serializer):
    resourceId = serializers.CharField(
        help_text="ID of resource",
        required=True,
        max_length=255,
        allow_null=True)
    vimId = serializers.CharField(
        help_text="ID of VIM",
        required=False,
        max_length=255,
        allow_null=True)
    resourceProviderId = serializers.CharField(
        help_text="ID of resource provider",
        required=False,
        max_length=255,
        allow_null=True)


class ExtVirtualLinkInfoSerializer(serializers.Serializer):
    extVirtualLinkId = serializers.CharField(
        help_text="ID of ext virtual link",
        required=True,
        max_length=255,
        allow_null=True)
    resourceHandle = ResourceHandleSerializer(
        help_text="Resource handle",
        required=True)
    linkPorts = LinkPortsSerializer(
        help_text="Link ports",
        many=True,
        allow_null=True)


class L3AddressDataSerializer(serializers.Serializer):
    iPAddressType = serializers.ChoiceField(
        help_text="IP address type",
        choices=['IPv4', 'IPv6'],
        required=True)
    iPAddress = serializers.CharField(
        help_text="IP address",
        required=True,
        max_length=255,
        allow_null=True)


class NetworkAddressSerializer(serializers.Serializer):
    addressType = serializers.ChoiceField(
        help_text="Address type",
        choices=['MAC', 'IP'],
        required=True)
    l2AddressData = serializers.CharField(
        help_text="l2 address data",
        required=False,
        max_length=255,
        allow_null=True)
    l3AddressData = L3AddressDataSerializer(
        help_text="l3 address data",
        required=False)


class ExtCpInfoSerializer(serializers.Serializer):
    cpInstanceId = serializers.CharField(
        help_text="cpInstanceId",
        required=False,
        max_length=255,
        allow_null=True)
    cpdId = serializers.IntegerField(
        help_text="cpdId",
        required=True,
        allow_null=True)
    numDynamicAddresses = serializers.IntegerField(
        help_text="numDynamicAddresses",
        required=False,
        allow_null=True)
    addresses = NetworkAddressSerializer(
        help_text="addresses",
        many=True,
        allow_null=True)


class ScaleInfoSerializer(serializers.Serializer):
    aspectId = serializers.CharField(
        help_text="aspectId",
        required=True,
        max_length=255,
        allow_null=True)
    scaleLevel = serializers.IntegerField(
        help_text="scaleLevel",
        required=True,
        allow_null=True)


class InstantiatedVnfInfoSerializer(serializers.Serializer):
    flavourId = serializers.CharField(
        help_text="flavourId",
        required=True,
        max_length=255,
        allow_null=True)
    vnfState = serializers.ChoiceField(
        help_text="vnfState",
        choices=['STARTED', 'STOPPED'],
        required=True,
        allow_null=True)
    localizationLanguage = serializers.CharField(
        help_text="localizationLanguage",
        required=True,
        max_length=255,
        allow_null=True)
    scaleStatus = ScaleInfoSerializer(
        help_text="scaleStatus",
        many=True)
    extCpInfo = ExtCpInfoSerializer(
        help_text="extCpInfo",
        many=True)
    extVirtualLink = ExtVirtualLinkInfoSerializer(
        help_text="extVirtualLink",
        many=True)
    monitoringParameters = serializers.DictField(
        help_text="monitoringParameters",
        child=serializers.CharField(allow_blank=True),
        required=False,
        allow_null=True)
    vmInfo = VmResponseSerializer(
        help_text="vmInfo",
        many=True,
        allow_null=True)
    vimInfo = VimInfoSerializer(
        help_text="vimInfo",
        many=True,
        required=False,
        allow_null=True)
    vnfcResourceInfo = VnfcResourceInfoSerializer(
        help_text="vnfcResourceInfo",
        many=True)
    virtualLinkResourceInfo = VirtualLinkResourceInfoSerializer(
        help_text="virtualLinkResourceInfo",
        many=True)
    virtualStorageResourceInfo = VirtualStorageResourceInfoSerializer(
        help_text="virtualStorageResourceInfo",
        many=True)


class VnfInfoSerializer(serializers.Serializer):
    vnfInstanceId = serializers.CharField(
        help_text="vnfInstanceId",
        required=True,
        max_length=255,
        allow_null=True)
    vnfInstanceName = serializers.CharField(
        help_text="vnfInstanceName",
        required=True,
        max_length=255,
        allow_null=True)
    vnfInstanceDescription = serializers.CharField(
        help_text="vnfInstanceDescription",
        required=True,
        max_length=255,
        allow_null=True)
    onboardedVnfPkgInfoId = serializers.CharField(
        help_text="onboardedVnfPkgInfoId",
        required=False,
        max_length=255,
        allow_null=True)
    vnfdId = serializers.CharField(
        help_text="vnfdId",
        required=True,
        max_length=255,
        allow_null=True)
    vnfdVersion = serializers.CharField(
        help_text="vnfdVersion",
        required=False,
        max_length=255,
        allow_null=True)
    vnfSoftwareVersion = serializers.CharField(
        help_text="vnfSoftwareVersion",
        required=True,
        max_length=255,
        allow_null=True)
    vnfProvider = serializers.CharField(
        help_text="vnfProvider",
        required=False,
        max_length=255,
        allow_null=True)
    vnfProductName = serializers.CharField(
        help_text="vnfProductName",
        required=False,
        max_length=255,
        allow_null=True)
    vnfConfigurableProperties = serializers.CharField(
        help_text="vnfConfigurableProperties",
        required=False,
        max_length=255,
        allow_null=True)
    instantiationState = serializers.CharField(
        help_text="instantiationState",
        required=False,
        max_length=255,
        allow_null=True)
    extensions = serializers.CharField(
        help_text="extensions",
        required=False,
        max_length=255,
        allow_null=True)
    metadata = serializers.CharField(
        help_text="metadata",
        required=False,
        max_length=255,
        allow_null=True)
    instantiatedVnfInfo = InstantiatedVnfInfoSerializer(
        help_text="instantiatedVnfInfo",
        required=True)


class VnfsInfoSerializer(serializers.Serializer):
    resp_data = VnfInfoSerializer(
        help_text="the response data",
        many=True)


class VmInfoSerializer(serializers.Serializer):
    resp_data = VmResponseSerializer(
        help_text="the response data",
        many=True)


class FlavorResponseSerializer(serializers.Serializer):
    flavourid = serializers.CharField(
        help_text="flavourid",
        required=True,
        max_length=255,
        allow_null=True)
    vimid = serializers.CharField(
        help_text="vimid",
        required=True,
        max_length=255,
        allow_null=True)
    resouceid = serializers.CharField(
        help_text="resouceid",
        required=True,
        max_length=255,
        allow_null=True)
    tenant = serializers.CharField(
        help_text="tenant",
        required=True,
        max_length=255,
        allow_null=True)
    instid = serializers.CharField(
        help_text="instid",
        required=True,
        max_length=255,
        allow_null=True)
    name = serializers.CharField(
        help_text="name",
        required=True,
        max_length=255,
        allow_null=True)
    extraspecs = serializers.CharField(
        help_text="extraspecs",
        required=True,
        max_length=255,
        allow_null=True)
    create_time = serializers.CharField(
        help_text="create_time",
        required=True,
        max_length=255,
        allow_null=True)
    memory = serializers.IntegerField(
        help_text="memory",
        required=True,
        allow_null=True)
    vcpu = serializers.IntegerField(
        help_text="vcpu",
        required=True,
        allow_null=True)


class FlavorInfoSerializer(serializers.Serializer):
    resp_data = FlavorResponseSerializer(
        help_text="the response data",
        many=True)


class NetworkResponseSerializer(serializers.Serializer):
    networkid = serializers.CharField(
        help_text="networkid",
        required=True,
        max_length=255,
        allow_null=True)
    vimid = serializers.CharField(
        help_text="vimid",
        required=True,
        max_length=255,
        allow_null=True)
    resouceid = serializers.CharField(
        help_text="resouceid",
        required=True,
        max_length=255,
        allow_null=True)
    insttype = serializers.IntegerField(
        help_text="insttype",
        required=True,
        allow_null=True)
    instid = serializers.CharField(
        help_text="instid",
        required=True,
        max_length=255,
        allow_null=True)
    name = serializers.CharField(
        help_text="name",
        required=True,
        max_length=255,
        allow_null=True)


class NetworkInfoSerializer(serializers.Serializer):
    resp_data = NetworkResponseSerializer(
        help_text="the response data",
        many=True)


class SubnetResponseSerializer(serializers.Serializer):
    subnetworkid = serializers.CharField(
        help_text="subnetworkid",
        required=True,
        max_length=255,
        allow_null=True)
    vimid = serializers.CharField(
        help_text="vimid",
        required=True,
        max_length=255,
        allow_null=True)
    resouceid = serializers.CharField(
        help_text="resouceid",
        required=True,
        max_length=255,
        allow_null=True)
    networkid = serializers.CharField(
        help_text="networkid",
        required=True,
        max_length=255,
        allow_null=True)
    insttype = serializers.IntegerField(
        help_text="insttype",
        required=True,
        allow_null=True)
    instid = serializers.CharField(
        help_text="instid",
        required=True,
        max_length=255,
        allow_null=True)
    name = serializers.CharField(
        help_text="name",
        required=True,
        max_length=255,
        allow_null=True)
    cidr = serializers.CharField(
        help_text="cidr",
        required=True,
        max_length=255,
        allow_null=True)


class SubnetInfoSerializer(serializers.Serializer):
    resp_data = SubnetResponseSerializer(
        help_text="the response data",
        many=True)


class CpResponseSerializer(serializers.Serializer):
    cpinstanceid = serializers.CharField(
        help_text="cpinstanceid",
        required=True,
        max_length=255,
        allow_null=True)
    cpdid = serializers.CharField(
        help_text="cpdid",
        required=True,
        max_length=255,
        allow_null=True)
    cpinstancename = serializers.CharField(
        help_text="cpinstancename",
        required=True,
        max_length=255,
        allow_null=True)
    vlinstanceid = serializers.CharField(
        help_text="vlinstanceid",
        required=True,
        max_length=255,
        allow_null=True)
    ownertype = serializers.IntegerField(
        help_text="ownertype",
        required=True,
        allow_null=True)
    ownerid = serializers.CharField(
        help_text="ownerid",
        required=True,
        max_length=255,
        allow_null=True)
    relatedtype = serializers.IntegerField(
        help_text="relatedtype",
        required=True,
        allow_null=True)


class CpsInfoSerializer(serializers.Serializer):
    resp_data = CpResponseSerializer(
        help_text="the response data",
        many=True)


class VolumeResponseSerializer(serializers.Serializer):
    storageid = serializers.CharField(
        help_text="storageid",
        required=True,
        max_length=255,
        allow_null=True)
    vimid = serializers.CharField(
        help_text="vimid",
        required=True,
        max_length=255,
        allow_null=True)
    resouceid = serializers.CharField(
        help_text="resouceid",
        required=True,
        max_length=255,
        allow_null=True)
    insttype = serializers.IntegerField(
        help_text="insttype",
        required=True,
        allow_null=True)
    instid = serializers.CharField(
        help_text="instid",
        required=True,
        max_length=255,
        allow_null=True)
    storagetype = serializers.CharField(
        help_text="storagetype",
        required=True,
        max_length=255,
        allow_null=True)
    size = serializers.CharField(
        help_text="size",
        required=True,
        max_length=255,
        allow_null=True)


class VolumeInfoSerializer(serializers.Serializer):
    resp_data = VolumeResponseSerializer(
        help_text="the response data",
        many=True)
