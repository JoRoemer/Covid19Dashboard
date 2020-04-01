import datetime
from collections import namedtuple
import numpy as np


DataTuple = namedtuple('DataTuple', ['cases', 'deaths', 'recovered'])

class cached_property(object):
    """ 
    Descriptor (non-data) for building an attribute on-demand on first use.
    """
    def __init__(self, factory):
        """
        <factory> is called such: factory(instance) to build the attribute.
        """
        self._attr_name = factory.__name__
        self._factory = factory


    def __get__(self, instance, owner):
        # Build the attribute.
        attr = self._factory(instance)

        # Cache the value; hide ourselves.
        setattr(instance, self._attr_name, attr)

        return attr


def string_to_date(string):
    return datetime.datetime.strptime(string, '%m/%d/%y')


def date_to_string(date):
    return date.strftime('%m/%d/%y')


def rebin_table(df, step):
    length = len(df.columns)

    # First: Make a copy. Do not change actual data
    df = df.copy(deep=True)

    # Transform column names to strins
    df = df.rename({column : date_to_string(column) for column in df.columns}, axis=1)

    # Delete all columns which should be aggregated (result is already agregated, not delta per day
    # so just delete all columns in between). 
    # First create a list which columns should be kept, i.e., the ones every X days
    keep_array = np.arange(length - 1, -1, -step)
    keep_array = list(reversed(keep_array))

    # Get a list of all days shifted 1 up (start of interval for next bin)
    start_dates = df.columns[[val + 1 for val in keep_array[:-1]]]
    # First date must be saved seperately
    first_date = df.columns[0]

    # Delete columns not to be kept
    for i, name in enumerate(df.columns):
        if i not in keep_array:
            del df[name]

    # Create a list of the new names start-finish of period
    names = [first_date + '-' + df.columns[1]] + [start_dates[i-1] + '-' + df.columns[i+1] for i in range(0, len(df.columns) - 1)]

    # Rename df
    df = df.rename({old_name : name for old_name, name in zip(df.columns, names)}, axis=1)

    return df


def get_diff_table(df):
    # Clone df. This one will contain the differences between the different days saved in df
    df_diff = df.copy(deep=True)

    # Calc differences
    names = df_diff.columns
    for i in reversed(range(1, len(names))):
        df_diff[names[i]] = df_diff[names[i]].sub(df_diff[names[i-1]])

    return df_diff
