# Copyright (c) 2023 by Jan Brodersen (Armitxes, https://armitxes.net).
# This work is licensed under the GNU General Public License v3.0
# Refer to the "LICENSE" file at the root folder of this project for more information.

import typing
from datetime import datetime
from requests import Response
from dialfire.core import DialfireCore


class DialfireTenant(DialfireCore):

  def __init__(
    self,
    tenant_id: str,
    tenant_token: str,
  ) -> None:
    self.id: str = tenant_id
    self.token: str = tenant_token

  def request(
    self,
    suburl: str,
    method: typing.Literal['GET', 'POST', 'DELETE'],
    json_request_list: list[dict] = [],
  ) -> Response:
    return super(DialfireTenant, self).request(
      suburl=f'tenants/{self.id}/{suburl}',
      token=self.token,
      method=method,
      json_request_list=json_request_list,
    )
