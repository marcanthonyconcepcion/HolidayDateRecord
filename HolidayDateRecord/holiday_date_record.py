__author__ = "Marc Concepcion"
__copyright__ = "Copyright 2023, Marc Concepcion"
__credits__ = ["Marc Concepcion"]
__maintainer__ = "Marc Concepcion"
__email__ = "marcanthonyconcepcion@gmail.com"
__status__ = "Demo"


import csv
import datetime
import holidays
import io
import json
import pycountry


class HolidayDateRecord:
    @staticmethod
    def fetch_future(country, number_of_years_further, subdivision=None):
        return json.dumps(sorted({key.strftime("%Y-%m-%d"): value for key, value in holidays.country_holidays(
                        country=country,
                        subdiv=subdivision,
                        years=range(datetime.date.today().year,
                                    datetime.date.today().year+number_of_years_further)).items()}.items()), indent=4)

    @staticmethod
    def fetch_global_holidays_csv(number_of_years_further):
        file_name = 'global_holidays.csv'
        header = ['Country', 'Subdivision Name', 'Date', 'Holiday']
        delimiter = ','
        with io.open(file_name, mode='w', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(f=csv_file, fieldnames=header, delimiter=delimiter)
            writer.writeheader()
        locales = holidays.utils.list_supported_countries()
        for country, subdivisions in locales.items():
            if 0 == len(subdivisions):
                holiday_list = json.loads(HolidayDateRecord.fetch_future(
                    country=country, number_of_years_further=number_of_years_further))
                for holiday in holiday_list:
                    with io.open(file_name, mode='a', encoding="utf-8") as csv_file:
                        writer = csv.DictWriter(f=csv_file, fieldnames=header, delimiter=delimiter)
                        writer.writerow(dict(zip(header, [
                            pycountry.countries.get(alpha_2=country).name if pycountry.countries.get(alpha_2=country) is not None else country,
                            ' ',
                            holiday[0],
                            holiday[1]])))
            else:
                for subdivision in subdivisions:
                    holiday_list = json.loads(HolidayDateRecord.fetch_future(
                        country=country, number_of_years_further=number_of_years_further, subdivision=subdivision))
                    with io.open(file_name, mode='a', encoding="utf-8") as csv_file:
                        writer = csv.DictWriter(f=csv_file, fieldnames=header, delimiter=delimiter)
                        for holiday in holiday_list:
                            writer.writerow(dict(zip(header, [
                                pycountry.countries.get(alpha_2=country).name if pycountry.countries.get(alpha_2=country) is not None else country,
                                pycountry.subdivisions.get(code=country+'-'+subdivision).name if pycountry.subdivisions.get(code=country+'-'+subdivision) is not None else subdivision,
                                holiday[0],
                                holiday[1]])))

    @staticmethod
    def fetch_global_holidays(number_of_years_further):
        global_holidays = {}
        locales = holidays.utils.list_supported_countries()
        for country, subdivisions in locales.items():
            if 0 == len(subdivisions):
                global_holidays[country] = json.loads(HolidayDateRecord.fetch_future(
                    country=country, number_of_years_further=number_of_years_further))
            else:
                global_holidays[country] = {}
                for subdivision in subdivisions:
                    global_holidays[country][subdivision] = json.loads(HolidayDateRecord.fetch_future(
                        country=country, number_of_years_further=number_of_years_further, subdivision=subdivision))
        return json.dumps(global_holidays, indent=4)
