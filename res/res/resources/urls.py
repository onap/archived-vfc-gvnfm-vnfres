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
from rest_framework.urlpatterns import format_suffix_patterns

from res.resources import views
from res.resources.views import SwaggerJsonView

urlpatterns = [
    url(r'^openoapi/vnfres/v1/vnfs/(?P<vnfInstanceId>[0-9a-zA-Z\-\_]+)$', views.get_vnf, name='get_vnf'),
    url(r'^openoapi/vnfres/v1/vnfs$', views.get_vnfs, name='get_vnfs'),
    url(r'^'+'openoapi/vnfres/v1/(?P<vnfInstanceId>[0-9a-zA-Z\-\_]+)/vms$', views.get_vms, name='get_vms'),
    url(r'^'+'openoapi/vnfres/v1/(?P<vnfInstanceId>[0-9a-zA-Z\-\_]+)/flavors$', views.get_flavors, name='get_flavors'),
    url(r'^'+'openoapi/vnfres/v1/(?P<vnfInstanceId>[0-9a-zA-Z\-\_]+)/networks$', views.get_networks, name='get_networks'),
    url(r'^'+'openoapi/vnfres/v1/(?P<vnfInstanceId>[0-9a-zA-Z\-\_]+)/subnets$', views.get_subnets, name='get_subnets'),
    url(r'^'+'openoapi/vnfres/v1/(?P<vnfInstanceId>[0-9a-zA-Z\-\_]+)/cps$', views.get_cps, name='get_cps'),
    url(r'^'+'openoapi/vnfres/v1/(?P<vnfInstanceId>[0-9a-zA-Z\-\_]+)/volumes$', views.get_volumes, name='get_volumes'),
    url(r'^openoapi/vnfres/v1/swagger.json$', SwaggerJsonView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
