from HolidayDateRecord.holiday_date_record import HolidayDateRecord
import filecmp
import os


def test_fetch_holidays_for_next_thirty_years():
    actual_holidays_json = HolidayDateRecord.fetch_future('US', 30)
    expected_file = open("expected_us_holidays.json", "r")
    expected_holidays_json = expected_file.read()
    expected_file.close()
    assert expected_holidays_json == actual_holidays_json


def test_global_holidays():
    actual_global_holidays_json = HolidayDateRecord.fetch_global_holidays(30)
    expected_file = open("expected_global_holidays.json", "r")
    expected_global_holidays_json = expected_file.read()
    expected_file.close()
    assert expected_global_holidays_json == actual_global_holidays_json

def test_global_holidays_csv():
    HolidayDateRecord.fetch_global_holidays_csv(30)
    assert filecmp.cmp('expected_global_holidays.csv', 'global_holidays.csv')
    os.remove('global_holidays.csv')
