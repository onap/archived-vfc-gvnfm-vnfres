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

from django.conf.urls import url

from res.resources.views.get_networks_view import GetNetworksView
from res.resources.views.get_flavors_view import GetFlavorsView
from res.resources.views.get_vnfs_view import GetVnfView
from res.resources.views.get_vnfs_view import GetVnfsView
from res.resources.views.get_vms_view import GetVmsView
from res.resources.views import views
from res.resources.health_check_views import HealthCheckView

urlpatterns = [
    url(r'^api/vnfres/v1/vnfs/(?P<vnf_instance_id>[0-9a-zA-Z\-\_]+)$', GetVnfView.as_view(), name='get_vnf'),
    url(r'^api/vnfres/v1/vnfs$', GetVnfsView.as_view(), name='get_vnfs'),
    url(r'^api/vnfres/v1/(?P<vnf_instance_id>[0-9a-zA-Z\-\_]+)/vms$', GetVmsView.as_view(), name='get_vms'),
    url(r'^api/vnfres/v1/(?P<vnf_instance_id>[0-9a-zA-Z\-\_]+)/flavors$', GetFlavorsView.as_view(), name='get_flavors'),
    url(r'^api/vnfres/v1/(?P<vnf_instance_id>[0-9a-zA-Z\-\_]+)/networks$', GetNetworksView.as_view(), name='get_networks'),
    url(r'^api/vnfres/v1/(?P<vnfInstanceId>[0-9a-zA-Z\-\_]+)/subnets$', views.getSubnets.as_view(), name='get_subnets'),
    url(r'^api/vnfres/v1/(?P<vnfInstanceId>[0-9a-zA-Z\-\_]+)/cps$', views.getCps.as_view(), name='get_cps'),
    url(r'^api/vnfres/v1/(?P<vnfInstanceId>[0-9a-zA-Z\-\_]+)/volumes$', views.getVolumes.as_view(), name='get_volumes'),

    # health check
    url(r'^api/vnfres/v1/health_check$', HealthCheckView.as_view()),
]
