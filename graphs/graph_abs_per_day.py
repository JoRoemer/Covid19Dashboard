import pandas as pd
import numpy as np
import plotly.graph_objects as go
from _plotly_utils.colors import DEFAULT_PLOTLY_COLORS

import tools.util
import tools.data


class GraphRate(object):
    def __init__(self, data):
        self.data = data


    @tools.util.cached_property
    def data_per_day(self):
        data = tools.util.DataTuple(
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
    def figure(self):
        fig = go.Figure()
        for i, country in enumerate(self.countries):
            graph = go.Scatter(
                x=self.rate_data.columns,
                #x=self.rate_data.columns[1:],
                #y=self.rate_data.loc[self.rate_data['Country/Region'] == country].values[0][1:],
                y=self.rate_data.loc[country],
                name=country,
                mode='lines+markers',
                line_color=DEFAULT_PLOTLY_COLORS[i % 10],
                legendgroup=country,
                hovertext='rate (average over ' + str(self.step) + ' days)',
            )
            fig.add_trace(graph)
        fig.update_layout(
            margin=dict(t=10),
            xaxis_title='Date',
            yaxis_title='Relative Change / %',
            height=400,
            font=dict(
                size=18,
                color="#7f7f7f",
            ),
            paper_bgcolor='rgba(0,0,0,0)',
        )
        return fig
