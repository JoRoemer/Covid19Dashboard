import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np

import tools.util


class DataContainer(object):
    def __init__(self, filename_cases, filename_deaths, filename_recovered, filename_population):
        self.filename_cases = filename_cases
        self.filename_deaths = filename_deaths
        self.filename_recovered = filename_recovered
        self.filename_population = filename_population


    @staticmethod
    def prepare_df(filename):
        df = pd.read_csv(filename)
        del df['Lat']
        del df['Long']
        df = df.groupby('Country/Region', as_index=False).sum()
        df = df.replace('US', 'United States')
        df = df.rename({column : tools.util.string_to_date(column) for column in df.columns[1:]}, axis=1)
        df = df.set_index('Country/Region')
        return df


    @tools.util.cached_property
    def population(self):
        df = pd.read_csv(self.filename_population, sep='\t')
        df = df[df['rank'] != '-']
        df['name'] = df['name'].str.strip()
        df = df.set_index('name')
        return df


    @tools.util.cached_property
    def cases(self):
        return self.prepare_df(self.filename_cases)


    @tools.util.cached_property
    def deaths(self):
        return self.prepare_df(self.filename_deaths)


    @tools.util.cached_property
    def recovered(self):
        return self.prepare_df(self.filename_recovered)


    @tools.util.cached_property
    def date_min_formatted(self):
        return self.dates[0]


    @tools.util.cached_property
    def date_max_formatted(self):
        return self.dates[-1]


    @tools.util.cached_property
    def date_min(self):
        return -self.total_days


    @tools.util.cached_property
    def date_max(self):
        return 0


    @tools.util.cached_property
    def total_days(self):
        return len(self.dates)


    @tools.util.cached_property
    def dates(self):
        return self.cases.columns[1:]


    @tools.util.cached_property
    def total_cases(self):
        return self.cases.iloc[:,-1].sum()


    @tools.util.cached_property
    def total_deaths(self):
        return self.deaths.iloc[:,-1].sum()


    @tools.util.cached_property
    def total_recovered(self):
        return self.recovered.iloc[:,-1].sum()
