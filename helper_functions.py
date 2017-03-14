"""
These are some helper functions to perform Pandas tricks.
They were included here instead of the jupyter notebook
to keep the noteboo shorter.
"""

import numpy as np
import pandas as pd

def searched_per_day_by_group(df):
    """
    Returns the number of searches per day in group 'a' 
    and group 'b'
    
    :param: df (Pandas DataFrame):  DataFrame indexed by pandas.DateTime
    
    :returns: Series with the day and the number of searches
              in that day for 'group a' and 'group b'
    
    :rvalue: Pandas Series
    """
    return df.groupby([pd.TimeGrouper('D'),
                       'group']).apply(lambda row:
                                len(row[row['action'] == 'searchResultPage']))


def searched_per_day(df):
    """
    Returns the number of searches per day regardless of group
    
    :param: df (Pandas DataFrame):  DataFrame indexed by pandas.DateTime
    
    :returns: Series with the day and the percentage of searches in that day
    
    :rvalue: Pandas Series
    """
    return df.groupby([pd.TimeGrouper('D')]).apply(lambda row: 
                                  len(row[row['action'] == 'searchResultPage']))


def average_click_through_rate(df):
    """
    Returns the average number of clickthroughs per day
    
    :param: df (Pandas DataFrame):  DataFrame indexed by pandas.DateTime
    
    :returns: Series with the day and the percentage of clickthroughs 
              in that day 
    
    :rvalue: float
    """
    # click through by day
    CT_PerDay = df.groupby([pd.TimeGrouper('D')]).apply(lambda row: 
                                  len(row[row['action'] == 'visitPage']))
    
    Searches_PerDay = searched_per_day(df)
    
    Daily_Averages = CT_PerDay / Searches_PerDay
    
    return Daily_Averages.mean()


def average_click_through_rate_by_group(df):
    """
    Returns the average number of clickthroughs per day by group 'a' vs. 'b'
    
    :param: d: Pandas DataFrame indexed by pandas.DateTime
    
    :returns: Series with the day and the percentage of clickthroughs 
              in that day for 'group a' and 'group b'
    
    :rvalue: Pandas Series
    """
    Searches_PerDay_By_Group = searched_per_day_by_group(df)
    CT_PerDay_By_Group = df.groupby([pd.TimeGrouper('D'),
                                     'group']).apply(lambda row: 
                                               len(row[row['action'] == 'visitPage']))

    
    Daily_Averages_By_Group = CT_PerDay_By_Group / Searches_PerDay_By_Group

    # groupby the second entry in the multi-tuple index
    return Daily_Averages_By_Group.groupby(level=[1]).mean()

    
def average_zero_rate(df):
    """
    Returns the average daily number of searches that return zero results.
    
    :param: df: Pandas dataframe indexed by pandas.DateTime
    
    :returns: average daily percentage of searches that return zero results.
    
    :rvalue: float
    """
    Searches_PerDay = searched_per_day(df)
    
    zero_results = df.groupby([pd.TimeGrouper('D')]).apply(lambda row: 
                                                   len(row[row['n_results'] == 0]))
    
    perecent_zeros = zero_results / Searches_PerDay
    
    return perecent_zeros.mean()


def average_zero_rate_by_group(df):
    """
    Returns the average daily number of searches that have zero 
    results by group.
    
    :param: df: Pandas dataframe indexed by pandas.DateTime
    
    :returns: Series with the day and the percentage of searches 
              that return zero results
              in that day for 'group a' and 'group b'
              
    :rvalue: Pandas Series
    """
    Searches_PerDay_By_Group = searched_per_day_by_group(df)
    
    zero_results = df.groupby([pd.TimeGrouper('D')]).apply(lambda row: 
                                                   len(row[row['n_results'] == 0]))
    
    perecent_zeros = zero_results / Searches_PerDay_By_Group
    
    # groupby the second entry in the multi-tuple index
    return perecent_zeros.groupby(level=[1]).mean()


def get_sessions_with_n_results(df, nresults):
    """
    Returns a Pandas Series where values
    are percentages of sessions with n_results = nresults 
    and session_length in different session length intervals.
    
    :param: df (Pandas DataFrame) : The merged dataframe (df3)
    
    :param:  nresults (int) : The number of listed results from the
              search.
    
    :returns: Series of the percentage of sessions with 
              n_results = nresults with session times in different
              intervals.
              
    :rvalue: Pandas Series
    """
    bins = [0,10,30,60,90,120,150,180,210,240]
    time = 240
    for i in range(6):
        time += 60
        bins.append(time)
        
    results = df[df.n_results_end == nresults]
    num_sessions = results.shape[0]

    result_session_length = results['time_end'] - results['time_start']
    result_session_length = \
                    result_session_length.apply(lambda row: row.seconds)
    result_top_session_length = \
                    result_session_length.value_counts(bins=bins)

    result_top_session_length /= num_sessions
    
    return result_top_session_length