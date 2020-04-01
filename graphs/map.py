import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np
import datetime

import tools.util
import tools.data


class WorldMap(object):
    def __init__(self, data, geojson):
        self.data = data
        self.geojson_name = geojson


    @tools.util.cached_property
    def geojson(self):
        with open(self.geojson_name, 'r') as fp:
            geojson = json.load(fp)
        return geojson


    @tools.util.cached_property
    def date_marks(self):
        return {i + self.data.date_min : tools.util.date_to_string(self.data.cases.columns[i+1]) for i in range(0, self.data.total_days, 7)}


    @property
    def current_date(self):
        if not hasattr(self, '_current_date'):
            self._current_date = self.data.dates[-1]
        return self._current_date


    @current_date.setter
    def current_date(self, val):
        self._current_date = datetime.datetime.strptime(val.split('T')[0], '%Y-%m-%d')


    @tools.util.cached_property
    def max_value(self):
        return self.data.cases.select_dtypes(include=[np.number]).max().max()


    @property
    def scale(self):
        if not hasattr(self, '_scale'):
            self._scale = 'lin'
        return self._scale


    @scale.setter
    def scale(self, val):
        self._scale = val


    @property
    def figure(self):
        vals = self.data.cases[self.current_date]
        max_value = self.max_value
        colorbar = dict(
            title=dict(
                text='Number of Cases',
                side='right',
            ),
        )
        if self.scale == 'log':
            vals = np.log10(vals)
            n_digits = len(str(max_value))
            max_value = int('1' + '0' * n_digits)
            ticks = ['1' + '0' * x for x in range(n_digits + 1)]
            max_value = np.log10(max_value)
            colorbar['tickvals'] = list(range(n_digits + 1))
            colorbar['ticktext'] = ticks

        fig = go.Figure(go.Choroplethmapbox(geojson=self.geojson,
                                            locations=self.data.cases.index,
                                            z=vals,
                                            featureidkey='properties.name',
                                            colorscale='YlOrRd',
                                            zmin=0,
                                            zmax=max_value,
                                            text=self.data.cases[self.current_date],
                                            hoverinfo='location+text',
                                            colorbar=colorbar,
                                            ))
        fig.update_layout(
            mapbox_style="carto-positron",
            margin={"r":0,"t":0,"l":0,"b":0},
            height=400,
            clickmode='event+select',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(
                size=18,
                color="#7f7f7f",
            ),
        )

        return fig
