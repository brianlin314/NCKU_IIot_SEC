import dash_html_components as html
import dash_bootstrap_components as dbc

# 定義導航欄
img_path = '../assets/img' # ../ 代表上一層目錄
logo = f'{img_path}/logo.png' # 成功大學圖樣
github = f'{img_path}/github1.png'

navbar = dbc.Navbar( 
    [
        html.A( # A為連結功用
            # 利用 row, col 來控制排版
            dbc.Row(
                [
                    dbc.Col(html.Img(src = logo, height = "50px")), 
                ],
            ),
            href="https://www.ncku.edu.tw/",
        ),
        dbc.Col(style={'width': 4}),
        html.A(
            # 利用 row, col 來控制排版
            dbc.Row(
                dbc.Col(html.Img(src=github, height="50px")),
            ),
            href="https://github.com/brianlin314/dashboard",
        ),
    ],
    color="#8EA0A5",
    dark=True,
    sticky='top',
    style={'width':'100%','height':'80px'},
)