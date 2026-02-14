import dash
from dash import dcc
from dash import html
from datetime import datetime
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
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                start_date=min_date,
                end_date=max_date
            ),
        ], className='two columns'),
        html.Div([
            # выбор типа дрона
            html.H6('Выбор типов объектов:'),
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
        html.H6('События по районам, времени  и типам'),

        html.Div(  # график событий по районам
            children=dcc.Graph(
                id='event_region', config={"displayModeBar": True},
            ), className="twelve columns", ),
    ], className='row'),  # Графики столбчатые

    html.Br(),

    html.Div([  # Графики круговые

        html.Div(  # график событий по районам

            children=dcc.Graph(
                id='pie_region', config={"displayModeBar": True},
            ), className="four columns", ),
        html.Div(  # доля событий по дням
            children=dcc.Graph(
                id='pie_time', config={"displayModeBar": True},

            ), className="four columns", ),
        html.Div(  # график событий по типам дронов
            children=dcc.Graph(
                id='pie_type', config={"displayModeBar": True},
            ), className="four columns", ),

    ], className='row'),  # Графики круговые pie

])  # layout


@app.callback(
    [
        Output("event_region", "figure")
       # , Output("event_time", "figure")
       # , Output("event_type", "figure")
        , Output("pie_region", "figure")
        , Output("pie_time", "figure")
        , Output("pie_type", "figure")
    ],
    [
        Input("region_selector", "value"),
        Input("type_selector", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(region, type, start_date, end_date):
    start_date_f = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_f = datetime.strptime(end_date, '%Y-%m-%d')
    # Фильтрация по времени
    f_df_time = df_time.query('eventsdatetime >= @start_date_f and eventsdatetime <= @end_date_f')
    # Фильтрация по районам
    f_df_region = df_region.query('district in @region')
    # Фильтрация по типам объектов
    f_df_type = df_type.query('name in @type')

    # Столбчатые графики
    event_region_figure = {
        "data":  [go.Bar(x=f_df_region["district"],
                         y=f_df_region["eventcount"],
                         name='События по районам'),
                  go.Bar(x=f_df_time["eventsdatetime"],
                         y=f_df_time["eventcount"],
                         name='Время '),
                  go.Bar(x=f_df_type["name"],
                         y=f_df_type["eventcount"],
                         name='тип сорбытия '),
                  ],
        "layout": go.Layout(xaxis={'title': 'район, время,тип события',
                                   'showgrid': True,
                                   'gridcolor': 'white'},
                            yaxis={'title': 'События',
                                   'showgrid': True,
                                   'gridcolor': 'white'},
                            width=2250,
                            height=800,
                            plot_bgcolor='lightgray',
                            title_font=dict(size=20),
                            barmode = 'stack'
                            )
    }

    # Круговые графики

    pie_region_figure = {
        "data": [go.Pie(
            labels=f_df_region['district'],
            values=f_df_region["eventcount"],
            name='По районам',
        )],
        "layout": go.Layout()

    }

    pie_time_figure = {
        "data": [go.Pie(
            labels=f_df_time['eventsdatetime'],
            values=f_df_time["eventcount"],
            name='По времени',
        )],
        "layout": go.Layout()
    }

    pie_type_figure = {
        "data": [go.Pie(
            labels=f_df_type['name'],
            values=f_df_type["eventcount"],
            name='По nbgfv',
        )],
        "layout": go.Layout()
    }


    return event_region_figure, pie_region_figure, pie_time_figure, pie_type_figure
if __name__ == '__main__':
    app.run(debug=True)
