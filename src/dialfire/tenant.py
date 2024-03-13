# Copyright (c) 2023 by Jan Brodersen (Armitxes, https://armitxes.net).
# This work is licensed under the GNU General Public License v3.0
# Refer to the "LICENSE" file at the root folder of this project for more information.

import typing
from dialfire.core import DialfireCore, DialfireResponse


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
    data: str | dict | list[dict] = [],
    cursor: str = '',
    limit: int = 0,
  ) -> DialfireResponse:
    """Send HTTP request to the dialfire API server for tenant related queries.

    Args:
      suburl (str): Added behind the API tenant url
      token: Request related token
      method: HTTP method
      data (optional): Request parameters.
      files (optional): files to be uploaded
      cursor (optional): cursor of previous request
      limit (optional): maximum amount of results returned

    Returns:
      DialfireResponse: Response by the API
    """
    return super(DialfireTenant, self).request(
      suburl=f'tenants/{self.id}/{suburl}',
      token=self.token,
      method=method,
      data=data,
      cursor=cursor,
      limit=limit,
    )

  def get_campaigns(self) -> DialfireResponse:
    """Get all campaings related to the tenant."""
    return self.request(
      suburl='campaigns',
      method='GET',
    )

  # region: Users
  def get_users(self) -> DialfireResponse:
    """Get all users related to the tenant."""
    return self.request(
      suburl='users',
      method='GET',
    )

  def get_user(self, user_id: str) -> DialfireResponse:
    """Get user associated with the tenant.

    Args:
      user_id (str): ID of the user
    """
    return self.request(
      suburl=f'users/{user_id}',
      method='GET',
    )

  def create_user(self, data: dict) -> DialfireResponse:
    """Create user within the tenant.

    Args:
      user_id (str): ID of the user
    """
    return self.request(
      suburl='users/create',
      method='POST',
      data=data,
    )

  def update_user(self, user_id: str, data: dict) -> DialfireResponse:
    """Update user associated with the tenant.

    Args:
      user_id (str): ID of the user
    """
    return self.request(
      suburl=f'users/{user_id}/update',
      method='POST',
      data=data,
    )

  def delete_user(self, user_id: str) -> DialfireResponse:
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
  def add_user_to_team(self, user_id: str, team_id: str) -> DialfireResponse:
    """Add user to team associated with the tenant.

    Args:
      user_id (str): ID of the user
      team_id (str): ID of the team
    """
    return self.request(
      suburl=f'users/{user_id}/teams/{team_id}',
      method='POST',
    )

  def remove_user_from_team(self, user_id: str, team_id: str) -> DialfireResponse:
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
  def get_inbound_lines(self) -> DialfireResponse:
    """List inbound lines."""
    return self.request(
      suburl='lines',
      method='GET',
    )

  def get_inbound_line(
    self,
    line_id: str,
    data: list[dict] = [],
    cursor: str = '',
    limit: int = 0,
  ) -> DialfireResponse:
    """List inbound calls of specific line.

    Args:
      line_id (str): ID of the line
      data: query parameters. Valid: start, end
    """
    return self.request(
      suburl=f'lines/{line_id}/calls/',
      method='GET',
      cursor=cursor,
      limit=limit,
      data=data,
    )

  def get_line_stats(self) -> DialfireResponse:
    """Get inbound line statistics."""
    return self.request(
      suburl='lines/stats',
      method='GET',
    )

  def get_user_line_stats(self, user_id: str, data: dict) -> DialfireResponse:
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

  def add_line_callback(self, line_id: str, data: dict) -> DialfireResponse:
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
  def get_activity_reports(self, data: dict) -> DialfireResponse:
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

  def get_activity_report(self, user_id: str, report_id: str) -> DialfireResponse:
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
  def delete_all_donotcall(self, data: dict) -> DialfireResponse:
    """Delete all numbers from tenant dnc list (campaign dnc list are untouched)

    Data dict:
      date_from: df_datetime
      date_to: df_datetime
    """
    return self.request(
      suburl='donotcall/delete/all',
      method='POST',
      data=data,
    )
  # endregion
