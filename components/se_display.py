import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from database import get_db
from plot import area, bar, donut

# set donut chart top num
mitre_topNum = 5
mitre_title = f'Top {mitre_topNum} MITRE ATT&CKS'
agent_topNum = 5
donut_agent_title = f'Top {agent_topNum} agents'
bar_agent_title = f'Alerts evolution - Top {agent_topNum} agents'

CONFIG = {
    'staticPlot': False,     # True, False
    'scrollZoom': True,      # True, False
    'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
    'showTips': True,       # True, False
    'displayModeBar': True,  # True, False, 'hover'
    'watermark': False,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d','select2d'],
}

FIRST_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": 23,
    "margin-top": 35,
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'zIndex':1,
    'border':'1px black solid',
    'width': '50%',
    'zIndex':1,
}

SECOND_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": 23,
    "margin-top": 35,
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'zIndex':1,
    'border':'1px black solid',
    'width': '46%',
    'zIndex':1,
}

def update(startDate, endDate, freqs, id):
    # get chart
    area_fig = area.update(startDate, endDate, 'rule.level', freqs, 'Alert level evolution',id)

    # 若無資料
    if len(area_fig.data) == 0:
        no_data = [0 for i in range(4)]
        msg = html.H1('此區間無資料', style={'fontSize':40, 'margin-left':850, 'margin-top':100})
        no_data += [msg, '']
        no_data.insert(0, f'從 {startDate} 到 {endDate}')
        return no_data

    # 若有資料
    donut_mitre_fig = donut.update(startDate, endDate, 'rule.mitre.technique', mitre_title, mitre_topNum, id)
    donut_mitre_fig.update_layout(legend=dict(x=1.2)) # legend 會擋到 label, 故往右移
    donut_agent_fig = donut.update(startDate, endDate, 'agent.name', donut_agent_title, agent_topNum, id)
    bar_agent_fig = bar.se_update(startDate, endDate, freqs, 'agent.name', bar_agent_title, agent_topNum, id)

    area_graph = dcc.Graph(
        figure=area_fig,
        clickData=None, hoverData=None,
        config=CONFIG, style=FIRST_STYLE,
    )

    donut_mitre_graph = dcc.Graph(
        figure=donut_mitre_fig,
        clickData=None, hoverData=None,
        config=CONFIG, style=SECOND_STYLE,
    )

    donut_agent_graph = dcc.Graph(
        figure=donut_agent_fig,
        clickData=None, hoverData=None,
        config=CONFIG, style=SECOND_STYLE,
    )

    bar_agent_graph = dcc.Graph(
        figure=bar_agent_fig,
        clickData=None, hoverData=None,
        config=CONFIG, style=FIRST_STYLE,
    )

    first_row = [area_graph, donut_mitre_graph]
    second_row = [donut_agent_graph, bar_agent_graph]

    # get num
    posts = get_db.connect_db("hids")
    total = posts.count_documents({'$and':[{'timestamp': {"$gte":startDate}},
                                           {'timestamp': {"$lte":endDate}},
                                           {'agent.id':{"$eq":id}}]})

    level12 = posts.count_documents({'$and':[{'timestamp': {"$gte":startDate}},
                                             {'timestamp': {"$lte":endDate}},
                                             {'agent.id':{"$eq":id}},
                                             {'rule.level': {"$gte":12}}]})

    fail = posts.count_documents({'$and':[{'timestamp': {"$gte":startDate}},
                                          {'timestamp': {"$lte":endDate}},
                                          {'agent.id':{"$eq":id}},
                                          {'rule.groups': 'authentication_failed'}]})

    success = posts.count_documents({'$and':[{'timestamp': {"$gte":startDate}},
                                             {'timestamp': {"$lte":endDate}},
                                             {'agent.id':{"$eq":id}},
                                             {'rule.groups': 'authentication_success'}]})

    return [f'從 {startDate} 到 {endDate}', total, level12, fail, success, first_row, second_row]