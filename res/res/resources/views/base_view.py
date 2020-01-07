# Copyright @ 2020 China Mobile (SuZhou) Software Technology Co.,Ltd.
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

from rest_framework import status
from rest_framework.response import Response

from res.pub.exceptions import VNFRESException
from res.pub.exceptions import NotFoundException


logger = logging.getLogger(__name__)


def make_error_resp(status, detail):
    return Response(
        data={
            'status': status,
            'detail': detail
        },
        status=status
    )


def view_safe_call_with_log(logger):
    def view_safe_call(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except NotFoundException as e:
                logger.error(e.args[0])
                return make_error_resp(
                    detail=e.args[0],
                    status=status.HTTP_404_NOT_FOUND
                )
            except VNFRESException as e:
                logger.error(e.args[0])
                return make_error_resp(
                    detail=e.args[0],
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                logger.error(e.args[0])
                logger.error(traceback.format_exc())
                return make_error_resp(
                    detail='Unexpected exception',
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return wrapper

    return view_safe_call
