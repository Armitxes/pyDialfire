# Copyright (c) 2023 by Jan Brodersen (Armitxes, https://armitxes.net).
# This work is licensed under the GNU General Public License v3.0
# Refer to the "LICENSE" file at the root folder of this project for more information.

import typing
from datetime import datetime
from io import BufferedReader
from dialfire.core import DialfireCore, DialfireResponse


class DialfireCampaign(DialfireCore):
  """API interface for the Dialfire campaigns."""

  def __init__(
    self,
    campaign_id: str,
    token: str,
  ) -> None:
    """Initialize a new Dialfire tenant class instance.

    Args:
      campaign_id (str): ID of the campaign within dialfire.
      token (str): API token
    """
    self.id: str = campaign_id
    self.token: str = token

  def request(
    self,
    suburl: str,
    method: typing.Literal['GET', 'POST', 'PUT', 'DELETE'],
    data: str | dict | list[dict] = [],
    files: dict = {},
    cursor: str = '',
    limit: int = 0,
  ) -> DialfireResponse:
    """Send HTTP request to the dialfire API server for campaign related queries.

    Args:
      suburl: Added behind the API campaign url
      token: Request related token
      method: HTTP method
      data (optional): Request parameters.
      files (optional): files to be uploaded
      cursor (optional): cursor of previous request
      limit (optional): maximum amount of results returned

    Returns:
      DialfireResponse: Response by the API
    """
    return super(DialfireCampaign, self).request(
      suburl=f'campaigns/{self.id}/{suburl}',
      token=self.token,
      method=method,
      data=data,
      files=files,
      cursor=cursor,
      limit=limit,
    )

  def get_file(self, path: str) -> DialfireResponse:
    """Get a file from the resources folder of the campaign.

    The resources folder can contain sub-folders, too.
    Read access to the "public" subfolder is granted without authorization.
    So this can be used to externally reference public campaign resources, like for images in an email.

    Args:
      path: The path to the file, including the file name and its extension

    Returns:
      Response object
    """
    return self.request(
      suburl=f'resources/{path}',
      method='GET',
    )

  def put_file(self, filename: str, file: BufferedReader) -> DialfireResponse:
    """Upload a file to the resources folder of the campaign.

    Args:
      filename: The desired dialfire filename including its extension
      file: BufferedReader of the file to upload
    """
    return self.request(
      suburl=f'resources/{filename}',
      method='PUT',
      files={'data': (filename, file)},
    )

  def delete_file(self, path: str) -> DialfireResponse:
    """Delete a file from the resources folder of the campaign.

    Args:
      path: The path to the file, including the file name and its extension
    """
    return self.request(
      suburl=f'resources/{path}',
      method='DELETE',
    )

  def get_tasks(self) -> DialfireResponse:
    """Get all tasks for the campaign."""
    return self.request(
      suburl='tasks',
      method='GET',
    )

  def get_donotcall(self) -> DialfireResponse:
    """Get DNC list."""
    return self.request(
      suburl='donotcall',
      method='GET',
    )

  def delete_filtered_donotcall(
    self,
    data: list[dict] = [],
  ) -> DialfireResponse:
    """Delete all entries of the DNC list matching the filter."""
    return self.request(
      suburl='donotcall/delete',
      method='POST',
      data=data,
    )

  def delete_all_donotcall(
    self,
    date_from: datetime,
    date_to: datetime,
  ) -> DialfireResponse:
    """Delete all entries of the DNC list within the date range."""
    str_from = DialfireCampaign.df_datetime(date_from)
    str_to = DialfireCampaign.df_datetime(date_to)
    return self.request(
      suburl='donotcall/delete',
      method='POST',
      data=[
        {"values": [str_from], "field": "date_from"},
        {"values": [str_to], "field": "date_to"}
      ],
    )

  # region Contacts
  def get_contact_flat_view(
    self,
    contact_id: str,
  ) -> DialfireResponse:
    """Get a detailed view of a contact record including the task log.

    Args:
      contact_id: ID of the contact
    """
    return self.request(
      suburl=f'contacts/{contact_id}/flat_view',
      method='GET',
    )

  def get_contacts_flat_view(
    self,
    data: list[dict] = [],
  ) -> DialfireResponse:
    """Send a list of contact IDs (in JSON list format) to retrieve a batch of flat view records for those contacts."""
    return self.request(
      suburl='contacts/flat_view',
      method='POST',
      data=data,
    )

  def get_contacts(
    self,
    data: list[dict] = [],
    cursor: str = '',
    limit: int = 100,
  ) -> DialfireResponse:
    """Search for contacts inside a campaign.

    Args:
      data: Filter for dialfire field values. See example.
      cursor: Cursor value of the previous call.
      limit: Limit the response size.

    data example:
    [
      {
        "values": ["491"],
        "field": "$phone",
        "reverse":true,
        "operator": "GT"
      }
    ]
    """
    return self.request(
      suburl='contacts/filter',
      method='POST',
      data=data,
      cursor=cursor,
      limit=limit,
    )

  def create_contact(
    self,
    task_name: str,
    ref: str,
    phone: str,
    data: dict = {},
  ) -> DialfireResponse:
    """Create a new contact record in an existing task.

    The payload is a JSON object containing any number of fields.
    If a $ref field is provided this field can later be used as an external reference in addition to the $id field.

    Args:
      task_name: Dialfire task name
      ref: External reference - typically the record id used in an external CRM system
      phone: Phone number - preferably in E164 format, but will be re-formatted according to the country settings
      data: key, value dict. Key must match the field name to be updated with given value.
    """
    data.update({
      '$ref': ref,
      '$phone': phone,
    })

    return self.request(
      suburl=f'tasks/{task_name}/contacts/create',
      method='POST',
      data=data,
    )

  def update_contact(
    self,
    contact_id: str,
    data: dict = {},
  ) -> DialfireResponse:
    """Update an existing contact

    Args:
      contact_id: Dialfire contact id
      data (dict, optional): Dict of fields to update
    """
    return self.request(
      suburl=f'contacts/{contact_id}/update',
      method='POST',
      data=data,
    )
  # endregion
