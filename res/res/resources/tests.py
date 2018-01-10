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
            "vnfInstanceId": "1",
            "vnfInstanceName": "VNF1",
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
                "vmInfo": [],
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
                "vmid": "vm0",
                "vimid": "vim0",
                "resouceid": "res0",
                "insttype": 0,
                "instid": "01",
                "vmname": "v1",
                "operationalstate": None,
                "tenant": None,
                "is_predefined": 0,
                "security_groups": "sec0",
                "flavor_id": "flavor0",
                "availability_zone": "ava0",
                "server_group": "server0",
                "volume_array": "volume0",
                "metadata": "meta0",
                "nic_array": "nic0"
            }]
        }
        self.flavors_data = {
            "resp_data": [
                {
                    "extraspecs": "ext0",
                    "create_time": None,
                    "name": "fname0",
                    "vimid": "vim0",
                    "memory": 0,
                    "vcpu": 0,
                    "instid": "01",
                    "resouceid": "res0",
                    "flavourid": "fla0",
                    "tenant": None
                }
            ]
        }
        self.networks_data = {
            "resp_data": [{
                "networkid": "net0",
                "vimid": "vim0",
                "resouceid": "res0",
                "insttype": 0,
                "instid": "01",
                "name": "net_name0"
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
                "size": "0"
            }]
        }

    def tearDown(self):
        pass

    def test_get_vnf(self):
        vnf_inst_id = "1"
        NfInstModel(nfinstid=vnf_inst_id, nf_name="VNF1").save()
        StorageInstModel(storageid="s02", vimid="vim01", resouceid="resource01", insttype=1,
                         instid=vnf_inst_id, storagetype="desc01", size="ten").save()
        response = self.client.get("/api/vnfres/v1/vnfs/%s" % vnf_inst_id)
        self.failUnlessEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_data, response.data)

    def test_get_vnfs(self):
        for i in range(1):
            NfInstModel(nfinstid="%s" % i, nf_name="VNF%s" % i).save()
            StorageInstModel(storageid="s0%s" % i, vimid="vim0%s" % i, resouceid="resource0%s" % i,
                             insttype=1, instid="%s" % i, storagetype="desc%s" % i, size="ten").save()
        response = self.client.get("/api/vnfres/v1/vnfs")
        self.failUnlessEqual(status.HTTP_200_OK, response.status_code)

    def test_get_vms(self):
        NfInstModel(nfinstid="%s" % "01", nf_name="VFS%s" % "01").save()
        nfInst = NfInstModel.objects.get(pk="01")
        for i in range(1):
            VmInstModel(vmid="vm%s" % i, vimid="vim%s" % i, resouceid="res%s" % i, instid="%s" % nfInst.nfinstid,
                        insttype=0, vmname="v1", nic_array="nic%s" % i, metadata="meta%s" % i,
                        volume_array="volume%s" % i, server_group="server%s" % i, availability_zone="ava%s" % i,
                        flavor_id="flavor%s" % i, security_groups="sec%s" % i).save()
        response = self.client.get("/api/vnfres/v1/%s/vms" % nfInst.nfinstid)
        self.failUnlessEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.vms_data, response.data)

    def test_get_flavors(self):
        NfInstModel(nfinstid="%s" % "01", nf_name="VFS%s" % "01").save()
        nfInst = NfInstModel.objects.get(pk="01")
        for i in range(1):
            FlavourInstModel(flavourid="fla%s" % i, name="fname%s" % i, vcpu="%d" % i, instid="%s" % nfInst.nfinstid,
                             memory="%d" % i, extraspecs="ext%s" % i, vimid="vim%s" % i, resouceid="res%s" % i).save()
        response = self.client.get("/api/vnfres/v1/%s/flavors" % nfInst.nfinstid)
        self.failUnlessEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.flavors_data, response.data)

    def test_get_networks(self):
        for i in range(1):
            NetworkInstModel(networkid="net%s" % i, name="net_name%s" % i, vimid="vim%s" % i,
                             instid="%s" % self.nf_inst_id, resouceid="res%s" % i, insttype="%d" % i).save()
        response = self.client.get("/api/vnfres/v1/%s/networks" % self.nf_inst_id)
        self.failUnlessEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.networks_data, response.data)

    def test_get_subnets(self):
        for i in range(1):
            SubNetworkInstModel(subnetworkid="sub%s" % i, vimid="vim%s" % i, resouceid="res%s" % i,
                                networkid="net%s" % i, insttype="%d" % i, instid="%s" % self.nf_inst_id,
                                name="sub_name%s" % i, cidr="cidr%s" % i).save()
        response = self.client.get("/api/vnfres/v1/%s/subnets" % self.nf_inst_id)
        self.failUnlessEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.subnets_data, response.data)

    def test_get_cps(self):
        for i in range(1):
            CPInstModel(cpinstanceid="cp%s" % i, cpdid="cpd%s" % i, cpinstancename="cpinstname%s" % i,
                        vlinstanceid="vlinst%s" % i, ownertype="%d" % i, ownerid="%s" % self.nf_inst_id,
                        relatedtype="%d" % i).save()
        response = self.client.get("/api/vnfres/v1/%s/cps" % self.nf_inst_id)
        self.failUnlessEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.cps_data, response.data)

    def test_get_volumes(self):
        for i in range(1):
            StorageInstModel(storageid="st%s" % i, vimid="vim%s" % i, resouceid="res%s" % i, insttype="%d" % i,
                             instid="%s" % self.nf_inst_id, storagetype="stype%s" % i, size="%s" % i).save()
        response = self.client.get("/api/vnfres/v1/%s/volumes" % self.nf_inst_id)
        self.assertEqual(self.volumes_data, response.data)
        self.failUnlessEqual(status.HTTP_200_OK, response.status_code)

    def test_swagger_ok(self):
        resp = self.client.get("/api/vnfres/v1/swagger.json", format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.content)
