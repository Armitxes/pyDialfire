# Copyright (c) 2023 by Jan Brodersen (Armitxes, https://armitxes.net).
# This work is licensed under the GNU General Public License v3.0
# Refer to the "LICENSE" file at the root folder of this project for more information.

import requests
import typing
from datetime import datetime

BASE_API_URL = 'https://api.dialfire.com/api'


class DialfireCore:

  @staticmethod
  def _dialfire_datetime_format() -> str:
    """Get dialfire datetime format

    Returns:
        str: Dialfire datetime format
    """
    return '%Y-%m-%dT%H:%M:%S.%f'

  @staticmethod
  def to_datetime(dt: str) -> datetime:
    """Convert dialfire datetime string to python datetime object

    Args:
        dt (str): Dialfire datetime string

    Returns:
        datetime: Python datetime object
    """
    dt_format = DialfireCore._dialfire_datetime_format()
    dt = dt.removesuffix('Z')
    return datetime.strptime(dt, dt_format)

  @staticmethod
  def df_datetime(dt: datetime) -> str:
    """Convert python datetime object to dialfire datetime string

    Args:
        dt (datetime): Python datetime object

    Returns:
        str: Dialfire datetime string
    """
    dt_format = DialfireCore._dialfire_datetime_format()
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
    """Send HTTP request to the dialfire API server

    Args:
        suburl (str): Added behind the API base url
        token (str): Request related token
        method (typing.Literal[&#39;GET&#39;, &#39;POST&#39;, &#39;DELETE&#39;]): HTTP method
        data (dict, optional): Request parameters.
        json_request_list (list[dict], optional): Request parameters in JSON format.
        files (dict, optional): files to be uploaded

    Raises:
        Exception: When request failed.

    Returns:
        requests.Response: Response by the API
    """
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