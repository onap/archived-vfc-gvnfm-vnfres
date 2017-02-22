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
from django.test import TestCase, Client
from rest_framework import status

from res.pub.database.models import NfInstModel, StorageInstModel


class ResourceTest(TestCase):
    def setUp(self):
        self.client = Client()
        NfInstModel.objects.all().delete()
        self.test_data = {
            "vnfInstanceId": u'1',
            "vnfInstanceName": 'VNF1',
            "vnfInstanceDescription": None,
            "onboardedVnfPkgInfoId": None,
            "vnfdId": None,
            "vnfdVersion": None,
            "vnfSoftwareVersion": None,
            "vnfProvider": None,
            "vnfProductName": None,
            "vnfConfigurableProperties": {None},
            "instantiationState": None,
            "instantiatedVnfInfo": {
                "flavourId": None,
                "vnfState": None,
                "scaleStatus": [],
                "extCpInfo": [],
                "extVirtualLink": [],
                "monitoringParameters": {},
                "localizationLanguage": None,
                "vimInfo": [],
                "vnfcResourceInfo": [],
                "virtualLinkResourceInfo": [],
                "virtualStorageResourceInfo": [
                    {
                        "virtualStorageInstanceId": "s01",
                        "virtualStorageDescId": "desc01",
                        "storageResource": {
                            "vimId": "vim01",
                            "resourceId": "resource01"
                        }
                    }

                ]
            },
            "metadata": None,
            "extensions": None
        }

    def tearDown(self):
        pass
        
    def test_get_vnf(self):
        vnf_inst_id = "1"
        NfInstModel(nfinstid=vnf_inst_id, nf_name='VNF1').save()
        StorageInstModel(storageid='s01', vimid='vim01', resouceid='resource01', insttype=1,\
                         instid=vnf_inst_id, storageDesc='desc01').save()
        response = self.client.get("/openoapi/vnfres/v1/vnfs/%s" % vnf_inst_id)
        self.assertEqual(self.test_data, response.data)
        # self.failUnlessEqual(status.HTTP_200_OK, response.status_code)

    def test_get_vnfs(self):
        for i in range(1):
            NfInstModel(nfinstid='%s' % i, nf_name='VNF%s' % i).save()
            StorageInstModel(storageid='s0%s' % i, vimid='vim0%s' % i, resouceid='resource0%s' % i, insttype=1, instid='%s' % i, storageDesc='desc%s' % i).save()
        response = self.client.get("/openoapi/vnfres/v1/vnfs")
        # self.assertEqual(self.test_data, response.data)
        self.failUnlessEqual(status.HTTP_200_OK, response.status_code)