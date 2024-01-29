# Copyright (c) 2023 by Jan Brodersen (Armitxes, https://armitxes.net).
# This work is licensed under the GNU General Public License v3.0
# Refer to the "LICENSE" file at the root folder of this project for more information.

import requests
import typing
from datetime import datetime

BASE_API_URL = 'https://api.dialfire.com/api'


class DialfireCore:

  @staticmethod
  def to_datetime(dt: str) -> datetime:
    if not (dt and isinstance(dt, str)):
      raise Exception('Dialfire: Invalid datetime string: {dt}')
    
    dt_format = '%Y-%m-%dT%H:%M:%S.%f'
    dt = dt.removesuffix('Z')
    return datetime.strptime(dt, dt_format)

  @staticmethod
  def df_datetime(dt: datetime) -> str:
    dt_format = '%Y-%m-%dT%H:%M:%S.%f'
    return dt.strftime(dt_format)[:-3] + 'Z'

  def request(
    self,
    suburl: str,
    token: str,
    method: typing.Literal['GET', 'POST', 'DELETE'],
    data: dict = {},
    json_request_list: list[dict] = [],
    files: dict = {},
  ) -> requests.Response:
    suburl = f'/{suburl}'.replace('//', '/')
    res = requests.request(
      method=method,
      url=f'{BASE_API_URL}{suburl}',
      headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'text/plain'
      },
      data=data or None,
      json=json_request_list or None,
      files=files or None,
    )

    if res.status_code != 200:
      raise Exception(f'Dialfire API: {res.content}')
    
    return res