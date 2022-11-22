# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 18:33:25 2022

@author: PradyumnaLondhe
"""




import plotly.io as pio
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from datetime import date
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import pandas as pd
import os
import base64
import io
from datetime import datetime, timedelta
from time import mktime
import time
import numpy as np
import plotly.graph_objects as go
from itertools import cycle
from datetime import datetime as dt
import datetime
global df
pio.renderers.default = 'browser'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets,
           suppress_callback_exceptions=True)

os.chdir("E:\Work In Progress\Interval Data Analysis Excel Dashboard")

app.layout = html.Div([
    html.Div([html.H1('Interval Data Analysis Dashboard', style={'textAlign': 'center'}),
              html.Hr()]),
    html.Div([html.H2('Please upload the formatted CSV or Excel file here'),
              html.Hr(),

              dcc.Upload(
                  id='upload-data',
                  children=html.Div([
                      'Drag and Drop or ',
                      html.A('Select Files')
                  ]),
                  style={
                      'width': '100%',
                      'height': '60px',
                      'lineHeight': '60px',
                      'borderWidth': '1px',
                      'borderStyle': 'dashed',
                      'borderRadius': '5px',
                      'textAlign': 'center',
                      'margin': '10px'
                  },
                  # Allow multiple files to be uploaded
                  multiple=True
              ),

              html.Div(id='output-data-upload'),
              html.Button('Submit', id='submit-val', n_clicks=0),
              html.Div(id='output-div')
              ])
])


def parse_contents(contents, filename, date):
    global df
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)


    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))


    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            page_size=10
        ),
        html.Hr(),  # horizontal line
    ])


@app.callback(Output('output-div', 'children'),
              Input('submit-val', 'n_clicks'),
              )
def show(n):
    global df
    if (n / 2) == 0 or (n / 2) != 0:

        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        df['year'] = df['Timestamp'].dt.year
        df['month'] = df['Timestamp'].dt.month_name()
        df['day'] = df['Timestamp'].dt.day_name()
        df['time'] = df['Timestamp'].dt.time
        df['date'] = df['Timestamp'].dt.date
        df = df.set_index('Timestamp')
        return html.Div([

            html.Hr(),
            html.Div([

                html.Div([
                    html.H2('Consumption Pattern Vs OAT'),
                    html.Hr(),
                    html.H3('Please select the start date and end date:'),
                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed=date(2010, 1, 1),
                        max_date_allowed=datetime.datetime.now(),
                        initial_visible_month=date(2021, 7, 1),
                        start_date=datetime.datetime.now(),
                        end_date=datetime.datetime.now()),

                ], style={'width': '100%', 'display': 'inline-block'}),
                html.Div(id='output-container-date-picker-range'),
                dcc.Graph(id='consumption-OAT'),

            ]),
            html.Div([

                html.Div([
                    html.H2('Monthly Electricity Consumption'),
                    html.Hr(),
                    html.H3('Please select the year:'),
                    dcc.Dropdown(
                        df['year'].unique(),
                        value=str(max(df['year'])),
                        id='year-selected'
                    )], style={'width': '50%', 'display': 'inline-block'}),

                dcc.Graph(id='Monthly-Bar'),
            ]),
            html.Div([

                html.Div([
                    html.H2('Monthly Electricity Demand'),
                    html.Hr(),
                    html.H3('Please select the required year and month:'),
                    html.Div([
                        dcc.Dropdown(
                            df['year'].unique(),
                            value=str(max(df['year'])),
                            id='year-selected-Demand'
                        )], style={'width': '50%', 'display': 'inline-block'}),
                    html.Div([
                        dcc.Dropdown(
                            id='month-selected-Demand'
                        )], style={'width': '50%', 'display': 'inline-block'}),
                    dcc.Graph(id='Monthly-Bar-Demand')
                ]),
            ]),
            html.Div([

                html.Div([

                    html.H2('HeatMap for Monthly Consumption Pattern'),
                    html.Hr(),
                    html.H3('Please select the required year and month:'),
                    html.Div([
                        dcc.Dropdown(
                            df['year'].unique(),
                            value=str(max(df['year'])),
                            id='year-selected-HeatMap'
                        )], style={'width': '50%', 'display': 'inline-block'}),
                    html.Div([
                        dcc.Dropdown(
                            id='month-selected-HeatMap'
                        )], style={'width': '50%', 'display': 'inline-block'}),
                    dcc.Graph(id='Monthly-HeatMap'),

                ]),
            ]),
            html.Div([

                html.Div([

                    html.H2('Daily Consumption Profile'),
                    html.Hr(),
                    html.H3('Please select the date for the daily consumption pattern:'),
                    html.Div([
                        dcc.Dropdown(
                            df['year'].unique(),
                            value=str(max(df['year'])),
                            id='year-selected-Daily1'
                        )], style={'width': '30%', 'display': 'inline-block'}),
                    html.Div([
                        dcc.Dropdown(
                            id='month-selected-Daily1'
                        )], style={'width': '30%', 'display': 'inline-block'}),
                    html.Div([
                        dcc.Dropdown(
                            id='day-selected-Daily1'
                        )], style={'width': '30%', 'display': 'inline-block'}),
                    html.Hr(),
                    html.Div([
                        dcc.Graph(id='Daily-Consumption'),

                    ]),
                ]),
            ]),
        ])




@app.callback(

    Output('month-selected-HeatMap', 'options'),
    Input('year-selected-HeatMap', 'value'))
def update_dropdown(year):
    df_Selected_year = df.loc[df['year'] == year]
    months = df_Selected_year['month'].unique()
    return months


@app.callback(

    Output('Monthly-HeatMap', 'figure'),
    Input('month-selected-HeatMap', 'value'),
    Input('year-selected-HeatMap', 'value'))
def update_figure(month, year):
    df_Selected_year = df.loc[df['year'] == year]
    df_Selected = df_Selected_year.loc[df_Selected_year['month'] == month]
    df_Selected1 = df_Selected.pivot(index='date', columns='time')
    df_Selected2 = df_Selected1.iloc[:, 0:24]

    columns = []
    for i in range(24):
        columns.append(df_Selected2.columns[i][1])

    df_Selected2.columns = columns

    df_Selected2.reset_index(inplace=False)

    array = df_Selected2.to_numpy()

    dates_array = df_Selected2.index.values

    fig = go.Figure(data=[go.Heatmap(
        z=array,
        x=df_Selected2.columns,
        y=dates_array,
        colorscale='thermal')],
        layout = go.Layout(
            yaxis={'categoryarray': dates_array.tolist()}
            ))

    fig.update_layout(height=800,
                      title=' Energy Consumption(kWh)',
                      xaxis_nticks=24,
                      yaxis_nticks=32)
    fig.update_xaxes(title_text='<b>Time<b>')
    fig.update_yaxes(title_text='<b>Date<b>', autorange="reversed")
    fig.update_traces(name='Consumption(in kWh)', selector=dict(type='heatmap'))

    return fig


@app.callback(

    Output('consumption-OAT', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_figure(start_date, end_date):
    df2 = df.reset_index()
    Start_Date = dt.strptime(start_date, '%Y-%m-%d')
    End_Date = dt.strptime(end_date, '%Y-%m-%d')

    Lower_Limit_Date = (df2['Timestamp'].dt.date) >= dt.date(Start_Date)
    Upper_Limit_Date = (df2['Timestamp'].dt.date) <= dt.date(End_Date)
    between_two_dates = Lower_Limit_Date & Upper_Limit_Date

    df3 = df2.loc[between_two_dates]

    fig = make_subplots(specs=[[{'secondary_y': True}]])

    fig.add_trace(
        go.Scatter(x=df3['Timestamp'], y=df3['Consumption(kWh)'], mode='lines', name='Consumption(kWh)'),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=df3['Timestamp'], y=df3['OAT (°F)'], mode='lines', name='OAT'),
        secondary_y=True,
    )

    fig.update_layout(height=800)
    # Set x-axis title
    fig.update_xaxes(title_text="<b>TimeStamp<b>")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Consumption(kWh)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>OAT(°F)</b>", secondary_y=True)

    return fig


@app.callback(

    Output('Monthly-Bar', 'figure'),
    Input('year-selected', 'value'))
def update_figure(year):
    df_Selected = df.loc[df['year'] == year]
    df_Selected1 = df.loc[df['year'] == year - 1]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_Selected1['month'].unique(),
        y=df_Selected1.groupby(['month'])['Consumption(kWh)'].sum(),
        name=str(year - 1),
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=df_Selected['month'].unique(),
        y=df_Selected.groupby(['month'])['Consumption(kWh)'].sum(),
        name=str(year),
        marker_color='lightsalmon'
    ))

    fig.update_layout(height=800, title='Monthly Energy Consumption(kWh)')
    fig.update_xaxes(title_text='<b>Month<b>')
    fig.update_yaxes(title_text='<b>Consumption(kWh)<b>')

    return fig


@app.callback(

    Output('month-selected-Demand', 'options'),
    Input('year-selected-Demand', 'value'))
def update_dropdown(year):
    df_Selected_year = df.loc[df['year'] == year]
    months = df_Selected_year['month'].unique()
    return months


@app.callback(

    Output('Monthly-Bar-Demand', 'figure'),
    Input('month-selected-Demand', 'value'),
    Input('year-selected-Demand', 'value'))
def update_dropdown(month, year):
    df_Selected_year = df.loc[df['year'] == year]
    df_Selected_month = df_Selected_year.loc[df_Selected_year['month'] == month]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_Selected_month['date'].unique(),
        y=df_Selected_month.groupby(['date'])['Demand(kW)'].mean(),
        name='Demand',
        marker_color='blue'
    ))
    fig.update_layout(height=800, title='Monthly Energy Demand(kW)', xaxis_nticks=30,
                      yaxis_nticks=10)
    fig.update_xaxes(title_text='<b>Date<b>')
    fig.update_yaxes(title_text='<b>Demand(kW)<b>')
    return fig


@app.callback(

    Output('month-selected-Daily1', 'options'),
    Input('year-selected-Daily1', 'value'))
def update_dropdown(year):
    df_Selected_year = df.loc[df['year'] == year]
    months = df_Selected_year['month'].unique()
    return months


@app.callback(

    Output('day-selected-Daily1', 'options'),
    Input('month-selected-Daily1', 'value'),
    Input('year-selected-Daily1', 'value'))
def update_dropdown(month, year):
    df_Selected_year = df.loc[df['year'] == year]
    df_Selected_month = df_Selected_year.loc[df_Selected_year['month'] == month]
    days = df_Selected_month['date'].unique()

    return days


@app.callback(

    Output('Daily-Consumption', 'figure'),
    Input('day-selected-Daily1', 'value'),
    Input('month-selected-Daily1', 'value'),
    Input('year-selected-Daily1', 'value'))
def update_figure(day, month, year):
    day = datetime.date.fromisoformat(day)
    df_Selected_year = df.loc[df['year'] == year]
    df_Selected_month = df_Selected_year.loc[df_Selected_year['month'] == month]
    df_Selected_date = df_Selected_month.loc[df_Selected_month['date'] == day]

    fig = go.Figure([go.Scatter(x=df_Selected_date['time'], y=df_Selected_date['Consumption(kWh)'])])
    fig.update_layout(height=800,
                      title='Daily Energy Consumption(kWh)',
                      xaxis_nticks=24)
    fig.update_xaxes(title_text='<b>Time<b>')
    fig.update_yaxes(title_text='<b>Energy Consumption(kWh)<b>')
    return fig


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


if __name__ == '__main__':
    app.scripts.config.serve_locally = True
    app.css.config.serve_locally = True
    app.run_server(debug=True)
