# Copyright (c) 2023 by Jan Brodersen (Armitxes, https://armitxes.net).
# This work is licensed under the GNU General Public License v3.0
# Refer to the "LICENSE" file at the root folder of this project for more information.

import typing
from datetime import datetime
from requests import Response
from dialfire.core import DialfireCore


class DialfireTenant(DialfireCore):
  """API interface for the Dialfire tenants."""

  def __init__(
    self,
    tenant_id: str,
    token: str,
  ) -> None:
    """Initialize a new Dialfire tenant class instance.

    Args:
        tenant_id (str): ID of the tenant within dialfire.
        token (str): API token
    """
    self.id: str = tenant_id
    self.token: str = token

  def request(
    self,
    suburl: str,
    method: typing.Literal['GET', 'POST', 'DELETE'],
    data: dict = {},
    json_request_list: list[dict] = [],
  ) -> Response:
    """Send HTTP request to the dialfire API server for tenant related queries.

    Args:
        suburl (str): Added behind the API tenant url
        method (typing.Literal[&#39;GET&#39;, &#39;POST&#39;, &#39;DELETE&#39;]): HTTP method
        data (dict, optional): Request parameters.
        json_request_list (list[dict], optional): Request parameters in JSON format.
        files (dict, optional): files to be uploaded

    Returns:
        requests.Response: Response by the API
    """
    return super(DialfireTenant, self).request(
      suburl=f'tenants/{self.id}/{suburl}',
      token=self.token,
      method=method,
      data=data,
      json_request_list=json_request_list,
    )
  
  def get_campaigns(self) -> Response:
    """Get all campaings related to the tenant."""
    return self.request(
      suburl='campaigns',
      method='GET',
    )

  # region: Users
  def get_users(self) -> Response:
    """Get all users related to the tenant."""
    return self.request(
      suburl='users',
      method='GET',
    )

  def get_user(self, user_id: str) -> Response:
    """Get user associated with the tenant.

    Args:
      user_id (str): ID of the user
    """
    return self.request(
      suburl=f'users/{user_id}',
      method='GET',
    )

  def create_user(self, data: dict) -> Response:
    """Create user within the tenant.

    Args:
      user_id (str): ID of the user
    """
    return self.request(
      suburl=f'users/create',
      method='POST',
      data=data,
    )


  def update_user(self, user_id: str, data: dict) -> Response:
    """Update user associated with the tenant.

    Args:
      user_id (str): ID of the user
    """
    return self.request(
      suburl=f'users/{user_id}/update',
      method='POST',
      data=data,
    )

  def delete_user(self, user_id: str) -> Response:
    """Delete the user associated with the tenant.

    Args:
      user_id (str): ID of the user to be deleted
    """
    return self.request(
      suburl=f'users/{user_id}',
      method='DELETE',
    )
  # endregion

  # region Team
  def add_user_to_team(self, user_id: str, team_id: str) -> Response:
    """Add user to team associated with the tenant.

    Args:
      user_id (str): ID of the user
      team_id (str): ID of the team
    """
    return self.request(
      suburl=f'users/{user_id}/teams/{team_id}',
      method='POST',
    )

  def remove_user_from_team(self, user_id: str, team_id: str) -> Response:
    """Remove the user from team associated with the tenant.

    Args:
      user_id (str): ID of the user
      team_id (str): ID of the team
    """
    return self.request(
      suburl=f'users/{user_id}/teams/{team_id}',
      method='DELETE',
    )
  # endregion

  # region: Lines
  def get_inbound_lines(self) -> Response:
    """List inbound lines."""
    return self.request(
      suburl='lines',
      method='GET',
    )
  
  def get_inbound_line(self, line_id: str, json_request_list: list[dict] = []) -> Response:
    """List inbound calls of specific line.
    
    Args:
      line_id (str): ID of the line
      json_request_list: query parameters. Valid: cursor, limit, start, end
    """
    return self.request(
      suburl=f'lines/{line_id}/calls/',
      method='GET',
      json_request_list=json_request_list,
    )

  def get_line_stas(self) -> Response:
    """Get inbound line statistics."""
    return self.request(
      suburl='lines/stats',
      method='GET',
    )

  def add_line_callback(self, line_id: str, data: dict) -> Response:
    """Create callback in inbound line.
    
    Args:
      line_id (str): ID of the line
      data (dict): payload. Valid keys: phoneNumber, instant, campaignId, contactId

    Data dict:
      phoneNumber (str): Phone number to be called back
      instant (bool): Indicates whether the customer should be called back immediately
      campaignId: optional ID of a campaign the contact with the specified phoneNumber should be searched within
      contactId: optional ID of the contact that should be opened when an agent accepts the call
    """
    return self.request(
      suburl=f'lines/{line_id}/callback',
      method='POST',
      data=data,
    )
  # endregion

  # region Activities
  def get_line_stas(self, data: dict) -> Response:
    """Fetch a list of activities of all users of the specified tenant.
    
    Data dict:
      start: earliest date of activities to fetch in the format 2023-01-27
      end: latest date of activities to fetch in the format 2023-01-27
    """
    return self.request(
      suburl='activities/reports',
      method='GET',
      data=data,
    )
  
  def get_user_line_stats(self, user_id: str, data: dict) -> Response:
    """Fetch a list of all activities of the specfied user.
    
    Args:
      user_id (str): ID of the user
      data (dict)

    Data dict:
      start: earliest date of activities to fetch in the format 2023-01-27
      end: latest date of activities to fetch in the format 2023-01-27
    """
    return self.request(
      suburl=f'users/{user_id}/activities/reports/',
      method='GET',
      data=data,
    )
  
  def get_activity_report(self, user_id: str, report_id: str) -> Response:
    """Fetch the activity report with the specified id.

    Args:
      user_id (str): ID of the user
      report_id (str): ID of the report
    """
    return self.request(
      suburl=f'users/{user_id}/activities/reports/{report_id}',
      method='GET',
    )
  # endregion

  # region DoNotCall
  def delete_all_donotcall(self, data: dict) -> Response:
    """Delete all numbers from tenant dnc list (campaign dnc list are untouched)
    
    Data dict:
      date_from: df_datetime
      date_to: df_datetime
    """
    return self.request(
      suburl=f'donotcall/delete/all',
      method='POST',
      data=data,
    )
  # endregion