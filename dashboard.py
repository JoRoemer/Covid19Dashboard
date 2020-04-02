# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq

from graphs.map import WorldMap
from graphs.graph_cases import GraphCases
from graphs.graph_rate import GraphRate
from graphs.graph_change_abs import GraphChangeAbs
from tools.data import DataContainer

data = DataContainer('data/time_series_covid19_confirmed_global.csv',
                     'data/time_series_covid19_deaths_global.csv',
                     'data/time_series_covid19_recovered_global.csv',
                     'data/population.csv')
#data = DataContainer('data/cases.csv', 'data/deaths.csv', 'data/recovered.csv', 'data/population.csv')
world_map = WorldMap(data, 'data/world.geo.json')
graph_cases = GraphCases(data)
graph_rate = GraphRate(data)
graph_change = GraphChangeAbs(data)

external_stylesheets = []

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H2('Covid-19', style={'textAlign': 'center', 'margin-bottom': '0px'}),
                        html.H5('Worldwide Overview', style={'textAlign': 'center'})
                    ],
                    className='four columns',
                    ),
                html.Div(
                    [
                        html.Div(
                            [html.H6(str(data.total_cases)), html.P('No. of Cases')],
                            id='total-cases',
                            className='pretty_container three columns',
                            ),
                        html.Div(
                            [html.H6(str(data.total_deaths)), html.P('No. of Deaths')],
                            id='total-deaths',
                            className='pretty_container three columns',
                            ),
                        html.Div(
                            [html.H6(str(data.total_recovered)), html.P('No. of Recoveries')],
                            id='total-recovered',
                            className='pretty_container three columns',
                            ),
                        html.Div(
                            [
                                html.Small(
                                    [
                                        'Data provided by ',
                                        html.A('Johns Hopkins University', href='https://github.com/CSSEGISandData/COVID-19'),
                                    ],
                                ),
                                html.Br(),
                                html.Small(
                                    [
                                        'Analysis code can be found on ',
                                        html.A('github', href='https://github.com/JoRoemer/Covid19Dashboard'),
                                    ],
                                ),
                            ],
                            className='mini_container three columns',
                        ),
                    ],
                className='eight columns',
                ),
            ],
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P('Select Scale'),
                                        daq.ToggleSwitch(
                                            id='scale-switch',
                                            label=['linear', 'lograrithmic'],
                                            value=False,
                                        ),
                                    ],
                                    className='five columns',
                                ),
                                html.Div(
                                    [
                                        html.P('')
                                    ],
                                    className='three columns',
                                ),
                                html.Div(
                                    [
                                        html.P('Select date'),
                                        dcc.DatePickerSingle(
                                            id='date-selection',
                                            min_date_allowed=data.date_min_formatted,
                                            max_date_allowed=data.date_max_formatted,
                                            date=data.date_max_formatted,
                                        )
                                    ],
                                    className='four columns',
                                ),
                            ],
                            className='row',
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P('Norm. to population'),
                                    ],
                                    className='four columns',
                                ),
                                html.Div(
                                    [
                                        daq.BooleanSwitch(id='norm-switch'),
                                    ],
                                    className='two columns',
                                ),
                            ],
                            className='row',
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P('Shift to common start'),
                                    ],
                                    className='four columns',
                                ),
                                html.Div(
                                    [
                                        daq.BooleanSwitch(id='shift-switch'),
                                    ],
                                    className='two columns',
                                ),
                                html.Div(
                                    [
                                        html.P('Separate Deaths'),
                                    ],
                                    className='four columns',
                                ),
                                html.Div(
                                    [
                                        daq.BooleanSwitch(id='shift-deaths-sep-switch'),
                                    ],
                                    className='two columns',
                                ),
                            ],
                            className='row',
                        ),
                        html.Div(
                            [
                                html.P('Data selection:'),
                            ],
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(''),
                                    ],
                                    className='one column',
                                ),
                                html.Div(
                                    [
                                        html.P('No. of Cases'),
                                    ],
                                    className='four columns',
                                ),
                                html.Div(
                                    [
                                        daq.BooleanSwitch(id='show-cases-switch', on=True),
                                    ],
                                    className='two columns',
                                ),
                            ],
                            className='row',
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(''),
                                    ],
                                    className='one column',
                                ),
                                html.Div(
                                    [
                                        html.P('No. of Deaths'),
                                    ],
                                    className='four columns',
                                ),
                                html.Div(
                                    [
                                        daq.BooleanSwitch(id='show-deaths-switch', on=True),
                                    ],
                                    className='two columns',
                                ),
                            ],
                            className='row',
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(''),
                                    ],
                                    className='one column',
                                ),
                                html.Div(
                                    [
                                        html.P('No. of Recoveries'),
                                    ],
                                    className='four columns',
                                ),
                                html.Div(
                                    [
                                        daq.BooleanSwitch(id='show-recovered-switch', on=True),
                                    ],
                                    className='two columns',
                                ),
                            ],
                            className='row',
                        ),
                        html.Div(
                            [
                                html.P('Average over Days'),
                            ],
                        ),
                        html.Div(
                            [
                                dcc.Slider(
                                    id='step-selection',
                                    min=1,
                                    max=10,
                                    marks={i : str(i) for i in range(1, 11)},
                                    value=1,
                                )
                            ],
                        ),
                    ],
                    className='pretty_container four columns',
                ),
                html.Div(
                    [
                        #dcc.Loading([
                            dcc.Graph(
                                id='world-map',
                            ),
                        #]),
                    ],
                    className='pretty_container eight columns'
                ),
            ],
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='cases-per-country',
                        )
                    ],
                    className='pretty_container six columns',
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id='rate-per-country',
                        ),
                    ],
                    className='pretty_container six columns',
                )
            ],
            className='row',
        ),
        html.Div(
            [
                dcc.Tabs(
                    [
                        dcc.Tab(label='Cases', value='tab-cases'),
                        dcc.Tab(label='Deaths', value='tab-deaths'),
                        dcc.Tab(label='Recovered', value='tab-recovered'),
                    ],
                    id='change-tabs',
                    value='tab-cases',
                ),
            ],
            className='twelve columns',
        ),
        html.Div(id='change-tabs-content', className='pretty_container twelve columns'),
    ]
)


@app.callback(
    Output('shift-deaths-sep-switch', 'disabled'),
    [Input('shift-switch', 'on')]
)
def update_separate_deaths_button(input_switch):
    return not input_switch


@app.callback(
    Output('world-map', 'figure'),
    [Input('date-selection', 'date'), Input('scale-switch', 'value')]
)
def update_map_date(input_date, input_scale):
    world_map.current_date = input_date
    input_scale = 'log' if input_scale else 'linear'
    world_map.scale = input_scale

    return world_map.figure


@app.callback(
    Output('cases-per-country', 'figure'),
    [Input('world-map', 'selectedData'),
     Input('scale-switch', 'value'),
     Input('norm-switch', 'on'),
     Input('shift-switch', 'on'),
     Input('show-cases-switch', 'on'),
     Input('show-deaths-switch', 'on'),
     Input('show-recovered-switch', 'on'),
     Input('shift-deaths-sep-switch', 'on'),]
)
def update_graph_cases(selected_data,
                       input_scale,
                       input_norm,
                       input_shift,
                       input_show_cases,
                       input_show_deaths,
                       input_show_recovered,
                       input_shift_deaths_sep):
    countries = [country['location'] for country in selected_data['points']] if selected_data is not None else []
    graph_cases.countries = countries
    input_scale = 'log' if input_scale else 'linear'
    graph_cases.scale = input_scale
    graph_cases.norm_to_population = input_norm
    graph_cases.shift_to_common_start = input_shift
    graph_cases.show_cases = input_show_cases
    graph_cases.show_deaths = input_show_deaths
    graph_cases.show_recovered = input_show_recovered
    graph_cases.separate_deaths = input_shift_deaths_sep

    return graph_cases.figure


@app.callback(
    Output('rate-per-country', 'figure'),
    [Input('world-map', 'selectedData'), Input('step-selection', 'value')]
)
def update_graph_rate(selected_data, step):
    countries = [country['location'] for country in selected_data['points']] if selected_data is not None else []
    graph_rate.countries = countries
    graph_rate.step = step

    return graph_rate.figure


@app.callback(
    Output('change-tabs-content', 'children'),
    [Input('world-map', 'selectedData'), Input('step-selection', 'value'), Input('change-tabs', 'value')]
)
def update_graph_change(selected_data, step, tab):
    countries = [country['location'] for country in selected_data['points']] if selected_data is not None else []
    graph_change.countries = countries
    graph_change.step = step
    graph_change.selected_table = tab

    return dcc.Graph(figure=graph_change.figure)


if __name__ == '__main__':
    app.run_server(debug=True)
