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
        length = len(self.data.dates)

        # First: Make a copy. Do not change actual data
        df = self.data.cases.copy(deep=True)

        # Transform column names to strins
        #df = df.rename({column : tools.util.date_to_string(column) for column in df.columns[1:]}, axis=1)
        df = df.rename({column : tools.util.date_to_string(column) for column in df.columns}, axis=1)

        # Delete all columns which should be aggregated (result is already agregated, not delta per day
        # so just delete all columns in betwee). 
        # First create a list which columns should be kept, i.e., the ones every X days
        keep_array = np.arange(length - self.step, 0, -self.step)
        keep_array = list(reversed(keep_array))
        #keep_array = [0] + [val for val in keep_array] + [length] # Region/Country
        keep_array = [val for val in keep_array] + [length] # Region/Country

        # Get a list of all days shifted 1 up (start of interval for next bin)
        #start_dates = df.columns[[val + 1 for val in keep_array[1:-1]]]
        start_dates = df.columns[[val + 1 for val in keep_array[:-1]]]
        # First date must be saved seperately
        first_date = df.columns[1]

        # Delete columns not to be kept
        for i, name in enumerate(df.columns):
            if i not in keep_array:
                del df[name]

        # Create a list of the new names start-finish of period
        #names = [first_date + '-' + df.columns[1]] + [start_dates[i-1] + '-' + df.columns[i+1] for i in range(1, len(df.columns) - 1)]
        names = [first_date + '-' + df.columns[1]] + [start_dates[i-1] + '-' + df.columns[i+1] for i in range(0, len(df.columns) - 1)]

        # Rename df
        #df = df.rename({old_name : name for old_name, name in zip(df.columns[1:], names)}, axis=1)
        df = df.rename({old_name : name for old_name, name in zip(df.columns, names)}, axis=1)

        # Clone df. This one will contain the differences between the different days saved in df
        df_diff = df.copy(deep=True)

        # Calc differences
        for i in reversed(range(1, len(names))):
            df_diff[names[i]] = df_diff[names[i]].sub(df_diff[names[i-1]])

        # Add a dummy column at the start of the df. Rates are relative to start date, not end date
        #df.insert(1, 'dummy', 0)
        df.insert(0, 'dummy', 0)

        # Common names for dividing
        #df_diff = df_diff.rename({name : i for i, name in enumerate(df_diff.columns[1:])}, axis=1)
        #df = df.rename({name : i for i, name in enumerate(df.columns[1:])}, axis=1)
        df_diff = df_diff.rename({name : i for i, name in enumerate(df_diff.columns)}, axis=1)
        df = df.rename({name : i for i, name in enumerate(df.columns)}, axis=1)

        # Divide both df's, scale with number of days and to percent
        #df_div = df_diff.iloc[:,1:].div(df.iloc[:,1:]) / self.step * 100
        df_div = df_diff.iloc[:,:].div(df.iloc[:,:]) / self.step * 100

        # Add region back
        #df_div.insert(0, 'Country/Region', df['Country/Region'])

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
