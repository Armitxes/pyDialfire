
from datetime import datetime
from unittest import TestCase
from dialfire.core import DialfireCore


class DateTimeConversion(TestCase):

  def test_datetime_to_df_string(self):
    dt_test: datetime = datetime.strptime(
      '2024-05-10 01:02:03.12745', '%Y-%m-%d %H:%M:%S.%f'
    )
    df_test = DialfireCore.df_datetime(dt_test)
    # Max. 3 floating point numbers
    self.assertEqual(df_test, '2024-05-10T01:02:03.127Z')

  def test_df_string_to_datetime(self):
    df_test = DialfireCore.to_datetime('2024-05-10T01:02:03.127Z')
    self.assertEqual(df_test.year, 2024)
    self.assertEqual(df_test.month, 5)
    self.assertEqual(df_test.day, 10)
    self.assertEqual(df_test.hour, 1)
    self.assertEqual(df_test.minute, 2)
    self.assertEqual(df_test.second, 3)
    self.assertEqual(df_test.microsecond, 127000)