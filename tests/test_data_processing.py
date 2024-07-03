import pandas as pd
import pytest

def test_crime_trend_graph():
    crime_data = {
        '2012': 4.7, '2013': 4.5, '2014': 4.4, '2015': 4.9,
        '2016': 5.4, '2017': 5.3, '2018': 5, '2019': 5.1,
        '2020': 6.5, '2021': 6.8, '2022': 6.3
    }
    years = list(crime_data.keys())
    numbers = list(crime_data.values())

    crime_trend = pd.DataFrame({'year': years, 'crime count': numbers})
    crime_trend['year'] = pd.to_numeric(crime_trend['year'])

    assert list(crime_trend['year']) == [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    assert list(crime_trend['crime count']) == [4.7, 4.5, 4.4, 4.9, 5.4, 5.3, 5, 5.1, 6.5, 6.8, 6.3]
