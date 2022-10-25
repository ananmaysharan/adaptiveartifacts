# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import Dash, dcc, html

external_stylesheets = 'https://rsms.me/inter/inter.css'

app = Dash(__name__, use_pages=True)
server = app.server

colors = {
    'background_blue': '#0128b900',
    'highlight_green': '#00ffbb',
    'light_green': '#e6fff8',
    'highlight_orange': '#FEA13D',
    'light_orange': '#ffeedc',
    'highlight_red': '#FF674E',
    'light_red': '#faecea',
    'highlight_yellow': '#F2D734',
    'text_black': '#212529'
}

app.layout = html.Div(style={'backgroundColor': colors['background_blue']}, children=[
    html.Div(style={'text-align': 'center', 'padding': '20px'}, className="logo", children=[
        html.Img(style={'width': '50%'}, src='/assets/adaptive-artifacts-logo.png')
    ]),

    html.Div(children='Data from April to September 2022', style={
        'textAlign': 'center',
        'color': 'white',
        'font-family': "'Inter', 'sans-serif'",
        'padding-bottom': '20px'
    }),

    html.Div(style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}, children=[
            html.Div(style={'padding': '20px'}, children=[
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"]
                )
                ]
            )
            for page in dash.page_registry.values()
        ]
    ),

    dash.page_container,
])
if __name__ == '__main__':
    app.run_server(debug=True)

