import dash_html_components as html
import feffery_antd_components as fac

# 定義左邊挑選欄位
# the style arguments for the sidebar. We use position : fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "50px",
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 0rem",
    "background-color": "#FFFFFF",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        fac.AntdSider(
            [
                html.Div(
                    [
                        fac.AntdMenu(
                            menuItems=[
                                {
                                    'component': 'Item',
                                    'props':{   
                                                'key': '/Home',
                                                'title': 'Home',
                                                'icon': 'antd-home',
                                                'href': '/Home',
                                            }
                                },
                                {
                                    'component': 'SubMenu', # submenu代表該按鈕"Host Based IDS"底下還有按鈕可以選擇
                                    'props':
                                            {  
                                                'key': '/Host_based',
                                                'title': 'Host IDS',
                                                'icon':'antd-folder-open'
                                            },
                                    'children': 
                                            [
                                                {
                                                    'component': 'Item',
                                                    'props': {
                                                        'key': '/Host_based/Discover',
                                                        'title': 'Discover',
                                                        'icon': 'antd-global',
                                                        'href': '/Host_based/Discover'
                                                    },
                                                },
                                                {
                                                    'component': 'Item',
                                                    'props': {
                                                        'key': '/Host_based/Security_events',
                                                        'title': 'Security Events',
                                                        'icon': 'antd-bar-chart',
                                                        'href': '/Host_based/Security_events'
                                                    },
                                                },
                                                {
                                                    'component': 'Item',
                                                    'props': {
                                                        'key': '/Host_based/logs',
                                                        'title': 'Events Logs',
                                                        'icon': 'antd-issues-close',
                                                        'href':'/Host_based/logs'
                                                    },
                                                },
                                            ]
                                },
                                {
                                    'component': 'SubMenu',
                                    'props': 
                                            {  
                                                'key': '/Network_based',
                                                'title': 'Network IDS',
                                                'icon': 'antd-partition'
                                            },
                                    'children': 
                                            [
                                                {
                                                    'component': 'Item',
                                                    'props': {
                                                        'key': '/Network_based/History',
                                                        'title': 'History',
                                                        'icon': 'antd-history',
                                                        'href': '/Network_based/History'
                                                    },
                                                },
                                                {
                                                    'component': 'Item',
                                                    'props': {
                                                        'key': '/Network_based/Statistics',
                                                        'title': 'Statistics',
                                                        'icon': 'antd-bar-chart',
                                                        'href': '/Network_based/Statistics'
                                                    },
                                                },
                                                {
                                                    'component': 'Item',
                                                    'props': {
                                                        'key': '/Network_based/logs',
                                                        'title': 'Events Logs',
                                                        'icon': 'antd-file-protect',
                                                        'href': '/Network_based/logs'
                                                    },
                                                }
                                            ]
                                },
                                {
                                    'component': 'Item',
                                    'props': 
                                            {  
                                                'key': '/AI_Prediction',
                                                'title': 'AI Prediction',
                                                'icon': 'antd-deployment-unit',
                                                'href': '/AI_Prediction'
                                            }
                                },
                                {
                                    'component': 'Item',
                                    'props': 
                                            {  
                                                'key': '/USB',
                                                'title': 'USB Logs',
                                                'icon': 'antd-database',
                                                'href': '/USB'
                                            }
                                },
                                {
                                    'component': 'SubMenu',
                                    'props': 
                                            {  
                                                'key': '/Setting',
                                                'title': 'Setting',
                                                'icon': 'antd-setting'
                                            },
                                    'children': [
                                        # {
                                        #     'component': 'Item',
                                        #     'props': {
                                        #         'key': '/Setting/add_agents',
                                        #         'title': 'Add/Delete Agents',
                                        #         'icon':'antd-user-add',
                                        #         'href':'/Setting/add_agents',
                                        #     },
                                        # },
                                        {
                                            'component': 'Item',
                                            'props': {
                                                'key': '/Setting/add_USB',
                                                'title': 'Add/Delete USB',
                                                'icon': 'antd-folder-add',
                                                'href': '/Setting/add_USB'
                                            },
                                        }
                                    ]
                                }
                            ],
                            mode='inline'
                        )
                    ],
                    style={
                        'height': '100%',
                        'overflowY': 'auto',
                    }
                )
            ],
            collapsible=True,
            style={
                'backgroundColor': 'rgb(240, 242, 245)'
            }
        ),
    ],
    id='sider-demo',
    style=SIDEBAR_STYLE
)
