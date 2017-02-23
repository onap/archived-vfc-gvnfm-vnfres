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

from res.pub.database.models import NfInstModel, StorageInstModel, VmInstModel, FlavourInstModel, NetworkInstModel, \
    SubNetworkInstModel, CPInstModel


class ResourceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.nf_inst_id = "01"
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
                        "virtualStorageInstanceId": "s02",
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
        self.vms_data = {
            "resp_data": [{
                "vmid": u"vm0",
                "vimid": u"vim0",
                "resouceid": u"res0",
                "insttype": 0,
                "instid": u"01",
                "vmname": u"v1",
                "operationalstate": None,
                "zoneid": None,
                "tenant": None,
                "hostid": None,
                "detailinfo": None,
                "is_predefined": 0
            }]
        }
        self.flavors_data = {
            "resp_data": [{
                "flavourid": "fla0",
                "name": "fname0",
                "vcpu": "cpu0",
                "memory": "mem0",
                "extraspecs": "ext0",
                "instid": "01",
                "tenant": None,
                "vmid": "vm0",
                "create_time": None
            }]
        }
        self.networks_data = {
            "resp_data": [{
                "networkid": "net0",
                "vimid": "vim0",
                "resouceid": "res0",
                "insttype": 0,
                "instid": "01",
                "name": "net_name0"
                # "tenant": None
            }]
        }
        self.subnets_data = {
            "resp_data": [{
                "subnetworkid": "sub0",
                "vimid": "vim0",
                "resouceid": "res0",
                "networkid": "net0",
                "insttype": 0,
                "instid": "01",
                "name": "sub_name0",
                "cidr": "cidr0"
            }]
        }
        self.cps_data = {
            "resp_data": [{
                "cpinstanceid": "cp0",
                "cpdid": "cpd0",
                "cpinstancename": "cpinstname0",
                "vlinstanceid": "vlinst0",
                "ownertype": 0,
                "ownerid": "01",
                "relatedtype": 0
            }]
        }

        self.volumes_data = {
            "resp_data": [{
                "storageid": "st0",
                "vimid": "vim0",
                "resouceid": "res0",
                "insttype": 0,
                "instid": "01",
                "storagetype": "stype0",
                "size": "0",
                "disktype": "disk0"
            }]
        }

    def tearDown(self):
        pass
        
    def test_get_vnf(self):
        vnf_inst_id = "1"
        NfInstModel(nfinstid=vnf_inst_id, nf_name='VNF1').save()
        StorageInstModel(storageid='s02', vimid='vim01', resouceid='resource01', insttype=1,\
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

    def test_get_vms(self):
        NfInstModel(nfinstid='%s' % '01', nf_name='VFS%s' % '01').save()
        nfInst = NfInstModel.objects.get(pk='01')
        for i in range(1):
            VmInstModel(vmid='vm%s' % i, vimid='vim%s' % i, resouceid='res%s' % i, instid='%s' % nfInst.nfinstid, insttype=0, vmname='v1').save()
        response = self.client.get("/openoapi/vnfres/v1/%s/vms" % nfInst.nfinstid)
        self.assertEqual(self.vms_data, response.data)
        # self.failUnlessEqual(status.HTTP_200_OK, response.status_code)

    def test_get_flavors(self):
        NfInstModel(nfinstid='%s' % '01', nf_name='VFS%s' % '01').save()
        nfInst = NfInstModel.objects.get(pk='01')
        for i in range(1):
            FlavourInstModel(flavourid='fla%s' % i, name='fname%s' % i, vcpu='cpu%s' % i, instid='%s' % nfInst.nfinstid, memory='mem%s' % i, extraspecs='ext%s' % i, vmid='vm%s' % i).save()
        response = self.client.get("/openoapi/vnfres/v1/%s/flavors" % nfInst.nfinstid)
        self.assertEqual(self.flavors_data, response.data)
        # self.failUnlessEqual(status.HTTP_200_OK, response.status_code)

    def test_get_networks(self):
        for i in range(1):
            NetworkInstModel(networkid='net%s' % i, name='net_name%s' % i, vimid='vim%s' % i, instid='%s' % self.nf_inst_id,
                             resouceid='res%s' % i, insttype='%d' % i).save()
        response = self.client.get("/openoapi/vnfres/v1/%s/networks" % self.nf_inst_id)
        self.assertEqual(self.networks_data, response.data)
        # self.failUnlessEqual(status.HTTP_200_OK, response.status_code)

    def test_get_subnets(self):
        for i in range(1):
            SubNetworkInstModel(subnetworkid="sub%s" % i, vimid='vim%s' % i, resouceid='res%s' % i, networkid='net%s' % i, insttype='%d' % i, instid='%s' % self.nf_inst_id, name='sub_name%s' % i, cidr="cidr%s" % i).save()
        response = self.client.get("/openoapi/vnfres/v1/%s/subnets" % self.nf_inst_id)
        self.assertEqual(self.subnets_data, response.data)
        # self.failUnlessEqual(status.HTTP_200_OK, response.status_code)

    def test_get_cps(self):
        for i in range(1):
            CPInstModel(cpinstanceid="cp%s" % i, cpdid='cpd%s' % i, cpinstancename='cpinstname%s' % i, vlinstanceid='vlinst%s' % i, ownertype='%d' % i, ownerid='%s' % self.nf_inst_id, relatedtype='%d' % i).save()
        response = self.client.get("/openoapi/vnfres/v1/%s/cps" % self.nf_inst_id)
        self.assertEqual(self.cps_data, response.data)
        # self.failUnlessEqual(status.HTTP_200_OK, response.status_code)

    def test_get_volumes(self):
        for i in range(1):
            StorageInstModel(storageid="st%s" % i, vimid='vim%s' % i, resouceid='res%s' % i, insttype='%d' % i, instid='%s' % self.nf_inst_id, storagetype='stype%s' % i, size='%s' % i, disktype='disk%s' % i).save()
        response = self.client.get("/openoapi/vnfres/v1/%s/volumes" % self.nf_inst_id)
        self.assertEqual(self.volumes_data, response.data)
        # self.failUnlessEqual(status.HTTP_200_OK, response.status_code)

    def test_swagger_ok(self):
        resp = self.client.get("/openoapi/vnfres/v1/resources/swagger.json", format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)