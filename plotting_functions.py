"""
This contains some functions to make plots that were a little
move involved. They are in this file to save space in the 
juptyer notebook.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

    
def plot_grouped_and_ungrouped(diff, rate, string):
    """
    Function that plots the Pandas Series values as bar graph. 
    
    :param: rate (float) : The value of the ungrouped results to 
                          be plotted.
                          
    :param: diff (Pandas Series) : The Series is usually the grouped 
                                   results.

    :param: string (str) : The description of the value to be plotted.
    """
    plt.figure(figsize=(4, 4))
    diff = diff.append(pd.Series([rate], index=['ungrouped']))
    diff.plot(kind='bar')
    plt.title(string)
    plt.xticks(rotation=0)
    plt.show()
    
    
def plot_daily_clicked(first_clicked, top_num):
    """
    Plots bar graphs of the daily number of clicks on the each search
    result by order of the listing.  The x-axis will be the ordering
    of the webpage search result and y-axis is the number of people's 
    whose first click was that result_position.  Each bar graph
    represents one of the eight days. 
    
    :param: first_clicked (Pandas Series) : This multi-index series.
            index level 0 - date
            index level 1 - session_id
            values - result_position
            
    :param: top_num (int): The number of web page clicks.
    """
    days = ['2016-03-01', '2016-03-02', '2016-03-03', '2016-03-04',
            '2016-03-05', '2016-03-06', '2016-03-07', '2016-03-08']

    day = 0
    string = ""
    plt.figure(figsize=(6, 7))
    for j in range(1,9):
        plt.subplot(4,2,j)
        # count the top 20 highest clicked links of this day
        day_clicked =\
            first_clicked[days[day]].value_counts().sort_index().head(top_num)
      
        plt.bar(day_clicked.index, day_clicked.values)
        plt.ylabel('Count')
        plt.title(days[day],fontsize=10)
        plt.xlabel('Result Position')
        plt.ylim([0,2500])
        day += 1
    
    plt.tight_layout()
    plt.show()

    
def plot_session_length_by_group(session_length_by_group):
    """
    Plots the frquency of sessions in group a and group b
    that have a session_length with in certain time inverals
    that were determined beforehand.
    
    :param: session_length_by_group (Pandas Series) : The frequency
                                        of session length by group.
    """
    plt.figure(figsize=(6,4))
    fig, ax = plt.subplots()
    rects1 = session_length_by_group['a'].sort_index().plot(kind='bar',
                                                        color='b',
                                                        label='Group a')
    
    rects2 = session_length_by_group['b'].sort_index().plot(kind='bar',
                                                        color='r',
                                                        label='Group b')
    plt.ylabel('Count Of Sessions')
    plt.xlabel('Session Length In Seconds')
    plt.title('Session Length Between The Groups')
    plt.legend()
    plt.show()
    

def plot_session_length_by_group_percentages(session_length_a,
                                             session_length_b):
    """
    Plots the percentages of sessions in group a and group b
    that had a session_length with in certain time inverals
    that were determined beforehand.
    
    
    :param: sesssion_length_a (Pandas Series) : 
    :param: sesssion_length_b(Pandas Series) : 
    """
    
    plt.figure(figsize=(9,5))
    plt.subplot(121)
    session_length_a.sort_index().plot(kind='bar',
                                    color='b',
                                    label='Group a')
    
    plt.title('Percentage Of Sessions By Session Length',
            fontsize=10)

    plt.ylim([0,0.25])
    plt.legend()
    plt.subplot(122)

    rects2 = session_length_b.sort_index().plot(kind='bar',
                                            color='r',
                                            label='Group b')
    
    plt.title('Percentage Of Sessions By Session Length',
            fontsize=10)

    plt.ylim([0,0.25])
    plt.legend()
    plt.show()