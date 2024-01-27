from datetime import datetime, timedelta

import dash_bootstrap_components as dbc
import feffery_antd_components as fac
from dash import html


# 新的 datepicker 統一 time format
def current_time():
    dateFormat = "%Y-%m-%d %H:%M:%S"
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    return yesterday, now

def date_picker(dsour):
    # 取得現在時間
    yesterday, now = current_time()
    # discover 的 date_picker
    date_picker = dbc.Row(
        [
            fac.AntdDateRangePicker(locale='en-us', showTime=True, defaultValue=[yesterday, now], id=dsour + '-datetime-picker'),
            html.Button('Update', id=dsour + '-submit-date', style={'margin-left':'1rem','height':'2rem'}, n_clicks=0),
        ],
        style={'margin-left':'5px'}
    )

    datetime_output = html.H6(id=dsour + '-datetime-output', style={'margin-top': '20px', 'margin-left': '7px'})

    date = dbc.Col(
        [
            date_picker,
            datetime_output,
        ],
    )
    return date

