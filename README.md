# pyDialfire
Python interface to Dialfire http://apidoc.dialfire.com/

## Development
Code documentation is provided by [typing](https://docs.python.org/3/library/typing.html) and DocString during development.

### Campaigns API
```python
from dialfire.campaign import DialfireCampaign

df_campaign = DialfireCampaign(campaign_id, token)
```

### Tenants API
```python
from dialfire.tenant import DialfireTenant

df_tenant = DialfireTenant(tenant_id, token)
```

### DateTime conversion
```python
from datetime import datetime
from dialfire.campaign import DialfireCampaign
from dialfire.tenant import DialfireTenant

# Convert dialfire datetime string to python datetime
py_dt: datetime = DialfireCampaign.to_datetime('2024-01-31T01:02:03.045Z')
py_dt: datetime = DialfireTenant.to_datetime('2024-01-31T01:02:03.045Z')

# Convert python datetime to dialfire datetime string
df_dt: str = DialfireCampaign.df_datetime(py_dt)  # -> 2024-01-31T01:02:03.045Z
df_dt: str = DialfireTenant.df_datetime(py_dt)  # -> 2024-01-31T01:02:03.045Z

```




Typing anCode documentation Google Python Style Guide