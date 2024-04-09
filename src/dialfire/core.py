# Copyright (c) 2023 by Jan Brodersen (Armitxes, https://armitxes.net).
# This work is licensed under the GNU General Public License v3.0
# Refer to the "LICENSE" file at the root folder of this project for more information.

import requests, typing
from datetime import datetime
from json.decoder import JSONDecodeError


BASE_API_URL = 'https://api.dialfire.com/api'


class DialfireRequest:

  def __init__(
    self,
    suburl: str,
    token: str,
    method: typing.Literal['GET', 'POST', 'PUT', 'DELETE'],
    data: str | dict | list[dict] = [],
    files: dict = {},
    cursor: str = '',
    limit: int = 0,
  ):
    """Send HTTP request to the dialfire API server

    Args:
      suburl: Added behind the API base url
      token: Request related token
      method: HTTP method
      data (optional): Request body
      files (optional): files to be uploaded
      cursor (optional): cursor of previous request
      limit (optional): maximum amount of results returned

    Raises:
      Exception: When request failed.
    """

    self.suburl = f'/{suburl}'.replace('//', '/')
    self.url = f'{BASE_API_URL}{self.suburl}'
    self.method = method
    self.token = token
    self.data = data
    self.files = files
    self.cursor = cursor
    self.limit = limit
    self.send()

  def send(self):
    data = self.data

    if isinstance(data, list):
      if self.cursor:
        data.append({"values": [str(self.cursor)], "field": "_cursor_"})

      if self.limit:
        data.append({"values": [str(self.limit)], "field": "_limit_"})

    res = requests.request(
      method=self.method,
      url=self.url,
      headers={
        'Authorization': f'Bearer {self.token}',
        'Content-Type': 'text/plain'
      },
      data=data if data and isinstance(data, str) else None,
      json=data if data and isinstance(data, (dict, list)) else None,
      files=self.files or None,
    )
    return DialfireResponse(request=self, response=res)


class DialfireResponse:

  def __init__(self, request: DialfireRequest, response: requests.Response):
    self.request = request
    self.headers = response.headers
    self.status_code = response.status_code
    self.text = response.text
    self.url = response.url
    self.json: dict[str, typing.Any] = {}
    self.matches: list = []
    self.cursor: str = ''
    self.limit: int = request.limit

    if self.status_code != 200:
      return

    try:
      self.json = response.json()

      # Cursor
      self.cursor = (
        self.json.get('cursor')
        or self.json.get('__cursor__')
        or ''
      )

      # Limit
      self.limit = (
        self.json.get('limit')
        or self.json.get('__limit__')
        or request.limit
      )

      # Matches / Hits
      self.matches = self.json.get('hits') or []

    except JSONDecodeError:
      return
    except ValueError:
      return
    except Exception:
      # There are too man JSONDecodeError exception sources
      # from json, simplejson, requests... too much to cover all.
      return

  def next_page(self) -> 'DialfireResponse':
    self.request.cursor = self.cursor
    return self.request.send()


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
    method: typing.Literal['GET', 'POST', 'PUT', 'DELETE'],
    data: str | dict | list[dict] = [],
    files: dict = {},
    cursor: str = '',
    limit: int = 0,
  ) -> DialfireResponse:
    """Send HTTP request to the dialfire API server

    Args:
      suburl: Added behind the API base url
      token: Request related token
      method: HTTP method
      data (optional): Request parameters.
      files (optional): files to be uploaded
      cursor (optional): cursor of previous request
      limit (optional): maximum amount of results returned

    Raises:
      Exception: When request failed.

    Returns:s
      DialfireResponse: Response by the API
    """
    res = DialfireRequest(
      suburl=suburl,
      token=token,
      method=method,
      data=data,
      files=files,
      cursor=cursor,
      limit=limit,
    )
    return res.send()
