import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import dash_mantine_components as dmc
import plotly.express as px
from rosely import WindRose as WR

external_stylesheets = 'https://rsms.me/inter/inter.css'

colors = {
    'background_blue': '#0d27b2',
    'highlight_green': '#00ffbb',
    'light_green': '#e6fff8',
    'highlight_orange': '#FEA13D',
    'light_orange': '#ffeedc',
    'highlight_red': '#FF674E',
    'light_red': '#faecea',
    'highlight_yellow': '#F2D734',
    'text_black': '#212529'

}

dash.register_page(
    __name__,
    path='/ws2',
    title='Weather Station 02',
    name='Weather Station 02'
)

# Wind Speed: WSP  Km/H
# Wind Direction: WDR °
# Temperature: TMP °C
# Humidity: HMD %
# Barometric Pressure: PRS HPa

# DATA MANIPULATION

# read data from file and create table, clean up formats

df = pd.read_csv("adaptive_artifacts_data_septend.csv", dtype={'event_date': 'string', 'sensor_id': 'string',
                                                               'sensor_value': 'string', 'event_type': 'string'})
df = df[~df.event_type.str.contains("CFT", na=False)]  # remove Comfort Scores
df["event_date"] = pd.to_datetime(df["event_date"])  # convert date column to date format
df["event_date_dp"] = df["event_date"].dt.date  # add new column with date
df["sensor_value"] = df["sensor_value"].astype(float)  # convert value column to float (number) format

# separate each weather station into different table

ws2 = df[df["sensor_id"] == "WeatherStation2"]


# manipulate tables to have sensor types as columns

ws2 = ws2.pivot_table(index=["event_date", "event_date_dp"], columns="event_type", values="sensor_value").reset_index()

layout = html.Div(children=[

    html.Div(id="ws2_temp", style={'background-color': '#ffffff', 'border': '5px solid',
                                   'border-color': colors['highlight_green'], 'padding': '20px', 'margin': '20px'},
             children=[

                 dcc.Graph(
                     id='ws2_temp_graph',
                 ),

                 dmc.DateRangePicker(
                     id='date-range-picker-tmp',
                     label="Date Range",
                     minDate=ws2["event_date_dp"].min(),
                     maxDate=ws2["event_date_dp"].max(),
                     value=[ws2["event_date_dp"].min(), ws2["event_date_dp"].max()],
                     style={"width": 310, 'padding': '0 0 0 0', 'font-family': "'Inter', 'sans-serif'"},
                     amountOfMonths=2,
                     hideOutsideDates=True,
                     clearable=False,
                     initialMonth="April",
                 ),
             ]),

    html.Div(id="ws2_hmd", style={'background-color': '#ffffff', 'border': '5px solid',
                                  'border-color': colors['highlight_orange'], 'padding': '20px', 'margin': '20px'},
             children=[

                 dcc.Graph(
                     id='ws2_hmd_graph',
                 ),

                 dmc.DateRangePicker(
                     id='date-range-picker-hmd',
                     label="Date Range",
                     minDate=ws2["event_date_dp"].min(),
                     maxDate=ws2["event_date_dp"].max(),
                     value=[ws2["event_date_dp"].min(), ws2["event_date_dp"].max()],
                     style={"width": 310, 'padding': '0 0 0 0', 'font-family': "'Inter', 'sans-serif'"},
                     amountOfMonths=2,
                     hideOutsideDates=True,
                     clearable=False,
                     initialMonth="April",
                 ),
             ]),

    html.Div(id="ws2_prs", style={'background-color': '#ffffff', 'border': '5px solid',
                                  'border-color': colors['highlight_red'], 'padding': '20px', 'margin': '20px'},
             children=[

                 dcc.Graph(
                     id='ws2_prs_graph',
                 ),

                 dmc.DateRangePicker(
                     id='date-range-picker-prs',
                     label="Date Range",
                     minDate=ws2["event_date_dp"].min(),
                     maxDate=ws2["event_date_dp"].max(),
                     value=[ws2["event_date_dp"].min(), ws2["event_date_dp"].max()],
                     style={"width": 310, 'padding': '0 0 0 0', 'font-family': "'Inter', 'sans-serif'"},
                     amountOfMonths=2,
                     hideOutsideDates=True,
                     clearable=False,
                     initialMonth="April",
                 ),
             ]),

    html.Div(id="ws2_wind", style={'background-color': '#ffffff', 'border': '5px solid',
                                   'border-color': colors['highlight_yellow'], 'padding': '20px', 'margin': '20px'},
             children=[

                 dcc.Graph(
                     id='ws2_wind_graph',
                 ),

                 dmc.DateRangePicker(
                     id='date-range-picker-wind',
                     label="Date Range",
                     minDate=ws2["event_date_dp"].min(),
                     maxDate=ws2["event_date_dp"].max(),
                     value=[ws2["event_date_dp"].min(), ws2["event_date_dp"].max()],
                     style={"width": 310, 'padding': '0 0 0 0', 'font-family': "'Inter', 'sans-serif'"},
                     amountOfMonths=2,
                     hideOutsideDates=True,
                     clearable=False,
                     initialMonth="April",
                 ),
             ]),
])


@callback(
    Output("ws2_temp_graph", "figure"),
    Input("date-range-picker-tmp", "value"),
)
def update_output_tmp(value):
    if value is not None:
        start_date = pd.to_datetime(value[0])
        end_date = pd.to_datetime(value[1])
        filtered_df_ws2 = ws2[(start_date <= ws2['event_date']) & (ws2['event_date'] <= end_date)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df_ws2["event_date"], y=ws2["TMP"], connectgaps=True, mode='lines',
                                 line=dict(color=colors['highlight_green']), name='lines'))
        fig.update_layout(title_text="WS2 Temperature", font_family="Inter", plot_bgcolor=colors['light_green'],
                          title_font_color=colors['text_black'], font_color=colors['text_black'])
        fig.update_xaxes(title_text='Time')
        fig.update_yaxes(title_text='Temperature (°C)')
        return fig


@callback(
    Output("ws2_hmd_graph", "figure"),
    Input("date-range-picker-hmd", "value"),
)
def update_output_hmd(value):
    if value is not None:
        start_date = pd.to_datetime(value[0])
        end_date = pd.to_datetime(value[1])
        filtered_df_ws2 = ws2[(start_date <= ws2['event_date']) & (ws2['event_date'] <= end_date)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df_ws2["event_date"], y=ws2["HMD"], connectgaps=True, mode='lines',
                                 line=dict(color=colors['highlight_orange']), name='lines'))
        fig.update_layout(title_text="WS2 Humidity", font_family="Inter", plot_bgcolor=colors['light_orange'],
                          title_font_color=colors['text_black'], font_color=colors['text_black'])
        fig.update_xaxes(title_text='Time')
        fig.update_yaxes(title_text='Humidity (%)')
        return fig


@callback(
    Output("ws2_prs_graph", "figure"),
    Input("date-range-picker-prs", "value"),
)
def update_output_prs(value):
    if value is not None:
        start_date = pd.to_datetime(value[0])
        end_date = pd.to_datetime(value[1])
        filtered_df_ws2 = ws2[(start_date <= ws2['event_date']) & (ws2['event_date'] <= end_date)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df_ws2["event_date"], y=ws2["PRS"], connectgaps=True, mode='lines',
                                 line=dict(color=colors['highlight_red']), name='lines'))
        fig.update_layout(title_text="WS2 Barometric Pressure", font_family="Inter", plot_bgcolor=colors['light_red'],
                          title_font_color=colors['text_black'], font_color=colors['text_black'])
        fig.update_xaxes(title_text='Time')
        fig.update_yaxes(title_text='WS2 Pressure (HPa)')
        return fig


@callback(
    Output("ws2_wind_graph", "figure"),
    Input("date-range-picker-wind", "value"),
)
def update_output_wind(value):
    if value is not None:
        start_date = pd.to_datetime(value[0])
        end_date = pd.to_datetime(value[1])
        ws2_WR_df = df[df["sensor_id"] == "WeatherStation1"]
        ws2_WR_df = ws2_WR_df.pivot_table(index="event_date", columns="event_type", values="sensor_value")
        # date filtering works for windrose but is a bit messy
        ws2_WR_df = ws2_WR_df.loc[start_date:end_date]
        ws2_WR_df = ws2_WR_df[['WSP', 'WDR']]
        ws2_WR_df = ws2_WR_df[(ws2_WR_df['WSP'] >= 0.05) | (ws2_WR_df['WSP'].isnull())]  # remove outliers / negatives
        ws2_WR_df.rename(columns={'WSP': 'ws', 'WDR': 'wd'}, inplace=True)
        ws2_WR = WR(ws2_WR_df)
        ws2_WR.calc_stats()

        fig = px.bar_polar(ws2_WR.wind_df, r="frequency", theta="direction",
                           color="speed", template="plotly_white",
                           color_discrete_sequence=px.colors.sequential.Plasma_r,
                           title="WS2 Wind Speed Distribution (Km/H)")
        fig.update_layout(title_font_color=colors['text_black'], font_color=colors['text_black'])
        return fig