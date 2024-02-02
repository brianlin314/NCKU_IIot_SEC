import dash_bootstrap_components as dbc
import globals_variable


def update_notification(first):
    if first == 1:
        posts = globals_variable.posts
        num = posts.count_documents({})
        notification = dbc.Alert(f'總共{num}筆', dismissable=True, is_open=True, duration=3000, style={'height': 40,'margin-right':'3rem', 'textAlign': 'center'})
        first = 0
    else:
        notification = dbc.Alert(f'新增{globals_variable.num}筆', dismissable=True, is_open=True, duration=3000, style={'height': 40})
    return first, notification