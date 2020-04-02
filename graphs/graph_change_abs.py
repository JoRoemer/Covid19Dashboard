import pandas as pd
import numpy as np
import plotly.graph_objects as go
from _plotly_utils.colors import DEFAULT_PLOTLY_COLORS
from plotly.subplots import make_subplots

import tools.util
import tools.data


class GraphChangeAbs(object):
    def __init__(self, data):
        self.data = data


    @staticmethod
    def get_rate(df1, df2):
        res = df1.div(df2) * 100
        return res.replace([np.inf, -np.inf, np.nan], 0.)


    @property
    def data_per_day(self):
        data = tools.util.DataTuple(
            cases=tools.util.get_diff_table(tools.util.rebin_table(self.data.cases, self.step)),
            deaths=tools.util.get_diff_table(tools.util.rebin_table(self.data.deaths, self.step)),
            recovered=tools.util.get_diff_table(tools.util.rebin_table(self.data.recovered, self.step)),
        )
        return data


    @property
    def rate_deaths(self):
        return self.get_rate(tools.util.rebin_table(self.data.deaths, self.step),
                             tools.util.rebin_table(self.data.cases, self.step))


    @property
    def rate_recovered(self):
        return self.get_rate(tools.util.rebin_table(self.data.recovered, self.step),
                             tools.util.rebin_table(self.data.cases, self.step))


    @property
    def countries(self):
        if not hasattr(self, '_countries'):
            self._countries = []
        return self._countries


    @countries.setter
    def countries(self, val):
        self._countries = val


    @property
    def step(self):
        if not hasattr(self, '_step'):
            self._step = 1
        return self._step


    @step.setter
    def step(self, val):
        self._step = val


    @property
    def selected_table(self):
        if not hasattr(self, '_selected_table'):
            self._selected_table = ''
        return self._selected_table


    @selected_table.setter
    def selected_table(self, val):
        self._selected_table = val


    @property
    def figure(self):
        if self.selected_table == 'tab-cases':
            fig = go.Figure()
            data_bar = self.data_per_day.cases
            data_line = None
        elif self.selected_table == 'tab-deaths':
            fig = make_subplots(specs=[[{'secondary_y': True}]])
            data_bar = self.data_per_day.deaths
            data_line = self.rate_deaths
        elif self.selected_table == 'tab-recovered':
            fig = make_subplots(specs=[[{'secondary_y': True}]])
            data_bar = self.data_per_day.recovered
            data_line = self.rate_recovered
        else:
            raise ValueError('Invalid tab selection ' % self.selected_table)

        for i, country in enumerate(self.countries):
            graph = go.Bar(
                x=data_bar.columns,
                y=data_bar.loc[country],
                name=country,
                marker_color=DEFAULT_PLOTLY_COLORS[i % 10],
                legendgroup=country,
            )
            fig.add_trace(graph)
            if data_line is not None:
                graph = go.Scatter(
                    x=data_line.columns,
                    y=data_line.loc[country],
                    name=country,
                    marker_color=DEFAULT_PLOTLY_COLORS[i % 10],
                    legendgroup=country,
                    showlegend=False,
                )
                fig.add_trace(graph, secondary_y=True)
        fig.update_layout(
            margin=dict(t=10),
            xaxis_title='Date',
            yaxis_title='Absolute Change',
            height=400,
            font=dict(
                size=18,
                color="#7f7f7f",
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            barmode='group',
            showlegend=True,
        )
        if data_line is not None:
            fig.update_yaxes(
                showgrid=False,
                title='Rate / %',
                secondary_y=True
            )
        return fig
