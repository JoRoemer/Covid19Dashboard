import pandas as pd
import numpy as np
import plotly.graph_objects as go
from _plotly_utils.colors import DEFAULT_PLOTLY_COLORS
from collections import namedtuple

import tools.util
import tools.data


class GraphCases(object):
    def __init__(self, data):
        self.data = data


    @property
    def countries(self):
        if not hasattr(self, '_countries'):
            self._countries = []
        return self._countries


    @countries.setter
    def countries(self, val):
        self._countries = val


    @property
    def scale(self):
        if not hasattr(self, '_scale'):
            self._scale = 'lin'
        return self._scale


    @scale.setter
    def scale(self, val):
        self._scale = val


    @property
    def norm_to_population(self):
        if not hasattr(self, '_norm_to_population'):
            self._norm_to_population = True
        return self._norm_to_population


    @norm_to_population.setter
    def norm_to_population(self, val):
        self._norm_to_population = val


    @property
    def shift_to_common_start(self):
        if not hasattr(self, '_shift_to_common_start'):
            self._shift_to_common_start = True
        return self._shift_to_common_start


    @shift_to_common_start.setter
    def shift_to_common_start(self, val):
        self._shift_to_common_start = val


    @property
    def show_cases(self):
        if not hasattr(self, '_show_cases'):
            self._show_cases = True
        return self._show_cases


    @show_cases.setter
    def show_cases(self, val):
        self._show_cases = val


    @property
    def show_deaths(self):
        if not hasattr(self, '_show_deaths'):
            self._show_deaths = True
        return self._show_deaths


    @show_deaths.setter
    def show_deaths(self, val):
        self._show_deaths = val


    @property
    def show_recovered(self):
        if not hasattr(self, '_show_recovered'):
            self._show_recovered = True
        return self._show_recovered


    @show_recovered.setter
    def show_recovered(self, val):
        self._show_recovered = val


    @property
    def separate_deaths(self):
        if not hasattr(self, '_separate_deaths'):
            self._separate_deaths = True
        return self._separate_deaths


    @separate_deaths.setter
    def separate_deaths(self, val):
        self._separate_deaths = val


    def norm_to_pupulation(self, df):
        return df.div(self.data.population['population'], axis=0).dropna(how='all') * 100000


    @tools.util.cached_property
    def shift_threshold_cases(self):
        return 100


    @tools.util.cached_property
    def shift_threshold_deaths(self):
        return 10


    @tools.util.cached_property
    def shift_values_cases(self):
        return (self.data.cases > self.shift_threshold_cases).idxmax(axis=1)


    @tools.util.cached_property
    def shift_values_deaths(self):
        return (self.data.deaths > self.shift_threshold_deaths).idxmax(axis=1)


    def shift_x(self, df, deaths=False):
        df = df.copy(deep=True)
        shift_values = self.shift_values_deaths if deaths else self.shift_values_cases
        shift_threshold = self.shift_threshold_deaths if deaths else self.shift_threshold_cases
        for index, row in df.iterrows():
            df.loc[index,:] = row.shift(-df.columns.get_loc(shift_values[index]))
        df[df < shift_threshold] = np.nan
        return df.rename(columns={name: i for i, name in enumerate(df.columns)})


    @tools.util.cached_property
    def data_per_population(self):
        data = tools.util.DataTuple(
            cases=self.norm_to_pupulation(self.data.cases),
            deaths=self.norm_to_pupulation(self.data.deaths),
            recovered=self.norm_to_pupulation(self.data.recovered)
        )
        return data


    @tools.util.cached_property
    def data_shifted_deaths_sep(self):
        data = tools.util.DataTuple(
            cases=self.shift_x(self.data.cases),
            deaths=self.shift_x(self.data.deaths, deaths=True),
            recovered=self.shift_x(self.data.recovered)
        )
        return data


    @tools.util.cached_property
    def data_shifted(self):
        data = tools.util.DataTuple(
            cases=self.shift_x(self.data.cases),
            deaths=self.shift_x(self.data.deaths),
            recovered=self.shift_x(self.data.recovered)
        )
        return data


    @tools.util.cached_property
    def data_shifted_per_population_deaths_sep(self):
        data = tools.util.DataTuple(
            cases=self.norm_to_pupulation(self.data_shifted.cases),
            deaths=self.norm_to_pupulation(self.data_shifted_deaths_sep.deaths),
            recovered=self.norm_to_pupulation(self.data_shifted.recovered)
        )
        return data


    @tools.util.cached_property
    def data_shifted_per_population(self):
        data = tools.util.DataTuple(
            cases=self.norm_to_pupulation(self.data_shifted.cases),
            deaths=self.norm_to_pupulation(self.data_shifted.deaths),
            recovered=self.norm_to_pupulation(self.data_shifted.recovered)
        )
        return data


    @property
    def data_to_plot(self):
        if self.norm_to_population and self.shift_to_common_start and self.separate_deaths:
            return self.data_shifted_per_population_deaths_sep
        if self.norm_to_population and self.shift_to_common_start and not self.separate_deaths:
            return self.data_shifted_per_population
        elif self.norm_to_population and not self.shift_to_common_start:
            return self.data_per_population
        elif not self.norm_to_population and self.shift_to_common_start and self.separate_deaths:
            return self.data_shifted_deaths_sep
        elif not self.norm_to_population and self.shift_to_common_start and not self.separate_deaths:
            return self.data_shifted
        else:
            return self.data


    @property
    def figure(self):
        fig = go.Figure()
        for i, country in enumerate(self.countries):
            if country in self.data_to_plot.cases.index and self.show_cases:
                graph_cases = go.Scatter(
                    x=self.data_to_plot.cases.columns,
                    y=self.data_to_plot.cases.loc[country],
                    name=country,
                    mode='lines+markers',
                    line_color=DEFAULT_PLOTLY_COLORS[i % 10],
                    legendgroup=country,
                    hovertext='confirmed cases',
                )
                fig.add_trace(graph_cases)
            if country in self.data_to_plot.deaths.index and self.show_deaths:
                graph_deaths = go.Scatter(
                    x=self.data_to_plot.deaths.columns,
                    y=self.data_to_plot.deaths.loc[country],
                    name=country,
                    mode='lines+markers',
                    line_color=DEFAULT_PLOTLY_COLORS[i % 10],
                    line=dict(dash='dash'),
                    legendgroup=country,
                    showlegend=False,
                    opacity=0.5,
                    hovertext='deaths',
                )
                fig.add_trace(graph_deaths)
            if country in self.data_to_plot.recovered.index and self.show_recovered:
                graph_recovered = go.Scatter(
                    x=self.data_to_plot.recovered.columns,
                    y=self.data_to_plot.recovered.loc[country],
                    name=country,
                    mode='lines+markers',
                    line_color=DEFAULT_PLOTLY_COLORS[i % 10],
                    line=dict(dash='dot'),
                    legendgroup=country,
                    showlegend=False,
                    opacity=0.5,
                    hovertext='recovered',
                )
                fig.add_trace(graph_recovered)
        fig.update_layout(
            yaxis_type=self.scale,
            margin=dict(t=10),
            xaxis_title='Date',
            yaxis_title='Number',
            height=400,
            font=dict(
                size=18,
                color="#7f7f7f",
            ),
            paper_bgcolor='rgba(0,0,0,0)',
        )
        if self.norm_to_population:
            fig.update_layout(yaxis_title='Number per 100k')
        return fig
