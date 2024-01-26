# Copyright (c) 2023 by Jan Brodersen (Armitxes, https://armitxes.net).
# This work is licensed under the GNU General Public License v3.0
# Refer to the "LICENSE" file at the root folder of this project for more information.

import typing
from datetime import datetime
from io import BufferedReader
from requests import Response
from dialfire.core import DialfireCore


class DialfireCampaign(DialfireCore):

  def __init__(
    self,
    campaign_id: str,
    token: str,
  ) -> None:
    self.id: str = campaign_id
    self.token: str = token

  def request(
    self,
    suburl: str,
    method: typing.Literal['GET', 'POST', 'DELETE'],
    json_request_list: list[dict] = [],
  ) -> Response:
    return super(DialfireCampaign, self).request(
      suburl=f'campaigns/{self.id}/{suburl}',
      token=self.token,
      method=method,
      json_request_list=json_request_list,
    )

  def get_file(self, path: str) -> Response:
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
  
  def put_file(self, filename: str, file: BufferedReader) -> Response:
    """Upload a file to the resources folder of the campaign.

    Args:
      filename: The desired dialfire filename including its extension
      file: BufferedReader of the file to upload
    """
    return self.request(
      suburl=f'resources/{filename}',
      method='PUT',
      file={'data': (filename, file)},
    )

  def delete_file(self, path: str) -> Response:
    """Delete a file from the resources folder of the campaign.

    Args:
      path: The path to the file, including the file name and its extension
    """
    return self.request(
      suburl=f'resources/{path}',
      method='DELETE',
    )

  def get_tasks(self) -> Response:
    """Get all tasks for the campaign."""
    return self.request(
      suburl='tasks',
      method='GET',
    )
  
  def get_donotcall(self) -> Response:
    """Get DNC list."""
    return self.request(
      suburl='donotcall',
      method='GET',
    )
  
  def delete_filtered_donotcall(
    self,
    json_request_list: list[dict] = [],
  ) -> Response:
    """Delete all entries of the DNC list matching the filter."""
    return self.request(
      suburl='donotcall/delete',
      method='POST',
      json_request_list=json_request_list,
    )
  
  def delete_all_donotcall(
    self,
    date_from: datetime,
    date_to: datetime,
  ) -> Response:
    """Delete all entries of the DNC list within the date range."""
    date_from = self.df_datetime(date_from)
    date_to = self.df_datetime(date_to)
    return self.request(
      suburl='donotcall/delete',
      method='POST',
      data={'date_from': date_from, 'date_to': date_to},
      json_request_list=[
        {"values": [date_from], "field": "date_from"},
        {"values": [date_to], "field": "date_to"}
      ],
    )

  def get_contact_flat_view(
    self,
    contact_id: str,
  ) -> Response:
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
    json_request_list: list[dict] = [],
  ) -> Response:
    """Send a list of contact IDs (in JSON list format) to retrieve a batch of flat view records for those contacts."""
    return self.request(
      suburl='contacts/flat_view',
      method='POST',
      json_request_list=json_request_list,
    )
  
  def get_contacts(
    self,
    json_request_list: list[dict] = [],
  ) -> Response:
    """Search for contacts inside a campaign.
    
    Args:
      json_request_list: Filter
        _cursor_: To iterate ALL contacts from campaign use _cursor_ and put in the value you got in response to the previous call.
        _limit_: Limit the response size.
    
    json_request_list example:
    [
      {
        "values": ["491"],
        "field": "$phone",
        "reverse":true,
        "operator": "GT"
      },
      {"values": ["1"], "field": "_limit_"}
    ]
    """
    return self.request(
      suburl='contacts/filter',
      method='POST',
      json_request_list=json_request_list,
    )
  
  def create_contact(
    self,
    task_name: str,
    ref: str,
    phone: str,
    data: dict = {},
    json_request_list: list[dict] = [],
  ) -> Response:
    """Create a new contact record in an existing task.
      
    The payload is a JSON object containing any number of fields.
    If a $ref field is provided this field can later be used as an external reference in addition to the $id field.

    Args:
      task_name: Dialfire task name
      ref: External reference - typically the record id used in an external CRM system
      phone: Phone number - preferably in E164 format, but will be re-formatted according to the country settings
    """
    data.update({
      '$ref': ref,
      '$phone': phone,
    })

    return self.request(
      suburl=f'tasks/{task_name}/contacts/create',
      method='POST',
      data=data,
      json_request_list=json_request_list,
    )
