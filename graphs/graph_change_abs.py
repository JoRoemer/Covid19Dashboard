import pandas as pd
import numpy as np
import plotly.graph_objects as go
from _plotly_utils.colors import DEFAULT_PLOTLY_COLORS

import tools.util
import tools.data


class GraphChangeAbs(object):
    def __init__(self, data):
        self.data = data


    @property
    def data_per_day(self):
        data = tools.util.DataTuple(
            cases=tools.util.get_diff_table(tools.util.rebin_table(self.data.cases, self.step)),
            deaths=tools.util.get_diff_table(tools.util.rebin_table(self.data.deaths, self.step)),
            recovered=tools.util.get_diff_table(tools.util.rebin_table(self.data.recovered, self.step)),
        )
        return data


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
    def figure(self):
        fig = go.Figure()
        for i, country in enumerate(self.countries):
            graph = go.Bar(
                x=self.data_per_day.cases.columns,
                y=self.data_per_day.cases.loc[country],
                name=country,
                marker_color=DEFAULT_PLOTLY_COLORS[i % 10],
            )
            fig.add_trace(graph)
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
        )
        return fig
