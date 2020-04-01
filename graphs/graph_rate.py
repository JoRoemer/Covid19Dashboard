import pandas as pd
import numpy as np
import plotly.graph_objects as go
from _plotly_utils.colors import DEFAULT_PLOTLY_COLORS

import tools.util
import tools.data


class GraphRate(object):
    def __init__(self, data):
        self.data = data


    @property
    def rate_data(self):
        # Rebin
        df = tools.util.rebin_table(self.data.cases, self.step)

        # Get diff
        df_diff = tools.util.get_diff_table(df)
        names = df_diff.columns

        # Add a dummy column at the start of the df. Rates are relative to start date, not end date
        df.insert(0, 'dummy', 0)

        # Common names for dividing
        #df_diff = df_diff.rename({name : i for i, name in enumerate(df_diff.columns[1:])}, axis=1)
        #df = df.rename({name : i for i, name in enumerate(df.columns[1:])}, axis=1)
        df_diff = df_diff.rename({name : i for i, name in enumerate(df_diff.columns)}, axis=1)
        df = df.rename({name : i for i, name in enumerate(df.columns)}, axis=1)

        # Divide both df's, scale with number of days and to percent
        #df_div = df_diff.iloc[:,1:].div(df.iloc[:,1:]) / self.step * 100
        df_div = df_diff.iloc[:,:].div(df.iloc[:,:]) / self.step * 100

        # Delete dummy column
        del df_div[df_div.columns[-1]]

        # Renname again to nice names
        df_div = df_div.rename({i : name for i, name in enumerate(names)}, axis=1)

        # Set all infs and NaNs to zero (from division)
        df_div.replace([np.inf, -np.inf, np.nan], 0.)

        return df_div


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
            graph = go.Scatter(
                x=self.rate_data.columns,
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
