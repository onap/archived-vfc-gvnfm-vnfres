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


class CpsResponseSerializer(serializers.Serializer):
    cpinstanceid = serializers.CharField(help_text="the cp instance id", required=True)
    cpdid = serializers.CharField(help_text="the cpd id", required=True)
    cpinstancename = serializers.CharField(help_text="the cp instance name of vnf", required=True)
    vlinstanceid = serializers.CharField(help_text="the vl instance id of vnf", required=True)
    ownertype = serializers.IntegerField(help_text="the owner type of vnf", required=True)
    ownerid = serializers.CharField(help_text="the owner id of vnf", required=True)
    relatedtype = serializers.IntegerField(help_text="the related type", required=True)


class CpsInfoSerializer(serializers.Serializer):
    resp_data = CpsResponseSerializer(help_text="the response data", many=True)


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
