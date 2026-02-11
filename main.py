import dash
from dash import dcc
from dash import html
from plotly import graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
from loaddata import min_date, max_date, df_region, df_time, df_type
pd.options.display.max_colwidth = 30
pd.options.display.float_format = '{:.2f}'.format

# Заголовок
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Распознавание воздушных объектов"

app.layout = html.Div(children=[
    html.Div([html.H1("События распознавания воздушных объектов")],
             className="row",
             style={'textAlign': "center"}),

    html.Div([  # Органы управления

        html.Div([
            # выбор временного периода
            html.H6('Период наблюдения:'),
            dcc.DatePickerRange(
                id="date-range",
                min_date_allowed = min_date,
                max_date_allowed = max_date,
                start_date = min_date,
                end_date = max_date
            ),
        ], className='two columns'),
        html.Div([
            # выбор типа дрона
            html.Label('Выбор типов объектов:'),
            dcc.Dropdown(
                options=[{'label': x, 'value': x} for x in df_type['name'].unique()],
                value=df_type['name'].unique().tolist(),
                multi=True,
                id='type_selector'
            ),
        ], className='four columns'),

        html.Div([
            # выбор района
            html.Label('Выбор районов наблюдения:'),
            dcc.Dropdown(
                options=[{'label': x, 'value': x} for x in df_region['district'].unique()],
                value=df_region['district'].unique().tolist(),
                multi=True,
                id='region_selector'
            ),
        ], className='six columns'),
    ], className='row'),

    html.Br(),

    html.Div([  # Графики столбчатые

        html.Div(  # график событий по районами
            children = dcc.Graph(
                id='event_region'
            ),className='six columns'),
        html.Div(  # график событий по дням
            children = dcc.Graph(
                id='event_time'
            ),className='six columns'),
        html.Div(  # график событий по типам дронов
            children = dcc.Graph(
                id='event_type'
            ),className='six columns'),

    ], className='row'),

])



@app.callback(
    [
            Output("event_region", "figure")
        , Output("event_time", "figure")
        , Output("event_type", "figure")
    ],

    [
        Input("region_selector", "value"),
        Input("type_selector", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)

def update_charts(region, type, start_date, end_date):

   # mask = (
    #        (df.region == region)
     #       & (df.type == avocado_type)
      #      & (df.Date >= start_date)
      #      & (df.Date <= end_date)
    #)
    #filtered_df = df.loc[mask, :]
    event_region_figure = {
        "data": [
            {
                "x": df_region["district"],
                "y": df_region["eventcount"],
                "type": "bar",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "События по районам",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    event_time_figure = {
        "data": [
            {
                "x": df_time["eventsdatetime"],
                "y": df_time["eventcount"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {
                "text": "События по суткам",
                "x": 0.05,
                "xanchor": "left"
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    event_type_figure = {
        "data": [
            {
                "x": df_type["name"],
                "y": df_type["eventcount"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {
                "text": "События по типам объектов",
                "x": 0.05,
                "xanchor": "left"
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }



    return event_region_figure , event_time_figure, event_type_figure

if __name__ == '__main__':
    app.run(debug=True)
