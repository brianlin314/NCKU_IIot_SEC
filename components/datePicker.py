import feffery_antd_components as fac
import dash_bootstrap_components as dbc
import dash_html_components as html
from datetime import datetime, timedelta

from components import alert

# 新的 datepicker 統一 time format
def current_time():
    dateFormat = "%Y-%m-%d %H:%M:%S"
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    return yesterday, now

def discover_date_picker():
    # 取得現在時間
    yesterday, now = current_time()
    print(yesterday, now)
    # discover 的 date_picker
    date_picker = dbc.Row(
        [
            fac.AntdDateRangePicker(locale='en-us', showTime=True, defaultValue=[yesterday, now], id='datetime-picker'),
            html.Button('Update', id='submit_date', style={'margin-left':'1rem','height':'2rem'}, n_clicks=0),
        ],
        style={'margin-left':'5px'}
    )

    datetime_output = html.H6(id='datetime-output', style={'margin-top': '20px', 'margin-left': '7px'})

    date = dbc.Col(
        [
            date_picker,
            datetime_output,
        ],
    )
    return date

def his_date_picker():
    # 取得現在時間
    yesterday, now = current_time()
    print(yesterday, now)
    # discover 的 date_picker
    hdate_picker = dbc.Row(
        [
            fac.AntdDateRangePicker(locale='en-us', showTime=True, defaultValue=[yesterday, now], id='hdatetime-picker'),
            html.Button('Update', id='hsubmit_date', style={'margin-left':'1rem','height':'2rem'}, n_clicks=0),
        ],
        style={'margin-left':'5px'}
    )

    hdatetime_output = html.H6(id='hdatetime-output', style={'margin-top': '20px', 'margin-left': '7px'})

    hdate = dbc.Col(
        [
            hdate_picker,
            hdatetime_output,
        ],
    )
    return hdate

def se_date_picker():
    # 取得現在時間
    yesterday, now = current_time()
    print(yesterday, now)
    # security events 的 date_picker (security events 簡稱 se)
    se_date_picker = dbc.Row(
        [
            fac.AntdDateRangePicker(locale='en-us', showTime=True, defaultValue=[yesterday, now], id='se-datetime-picker'),
            html.Button('Update', id='se-submit_date', style={'margin-left':'1rem'}, n_clicks=0),
        ],
        style={'margin-left':'5px'}
    )
    se_datetime_output = html.H6('', id='se-datetime-output', style={'margin-top': '20px', 'margin-left': '7px'})

    se_date = dbc.Col(
        [
            se_date_picker,
            se_datetime_output,
        ],
    )
    return se_date

def st_date_picker():
    # 取得現在時間
    yesterday, now = current_time()
    print(yesterday, now)
    # security events 的 date_picker (security events 簡稱 se)
    st_date_picker = dbc.Row(
        [
            fac.AntdDateRangePicker(locale='en-us', showTime=True, defaultValue=[yesterday, now], id='st-datetime-picker'),
            html.Button('Update', id='st-submit_date', style={'margin-left':'1rem'}, n_clicks=0),
        ],
        style={'margin-left':'5px'}
    )
    st_datetime_output = html.H6('', id='st-datetime-output', style={'margin-top': '20px', 'margin-left': '7px'})

    st_date = dbc.Col(
        [
            st_date_picker,
            st_datetime_output,
        ],
    )
    return st_date
