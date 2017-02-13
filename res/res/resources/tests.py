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

from res.pub.database.models import NfInstModel


class ResourceTest(TestCase):
    def setUp(self):
        self.client = Client()
        NfInstModel.objects.all().delete()

    def tearDown(self):
        pass
        
    def test_get_vnf(self):
        vnf_inst_id = "1"
        NfInstModel(nfinstid=vnf_inst_id, nf_name='VNF1').save()
        response = self.client.get("/openoapi/vnfres/v1/vnfs/%s" % vnf_inst_id)
        self.failUnlessEqual(status.HTTP_200_OK, response.status_code)
