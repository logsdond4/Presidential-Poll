# -*- coding: utf-8 -*-
"""
Author: Dan Logsdon
Date: 10/09/2020

This code uses open source data obtained from:
https://github.com/fivethirtyeight/data/tree/master/polls

This file calculates the weighted percentage score for each candidate for the general election
and calculates the overall candidate lead percentage.

"""

##%% Package Import
import pandas as pd
import os
import numpy as np
import statistics

#%% Import Data
root = os.path.dirname(os.path.dirname(__file__)) #root folder
src = root + '\\src' #source folder
file = src + '\\president_polls.csv' #input file
df=pd.read_csv(file)

#%% Functions
# This function cleans the dataset (e.g., removing NA values, data conversion)
def df_clean(df): 
    df['end_date'] = pd.to_datetime(df['end_date'])
    df = df[df['sample_size'].notna()]
    
    return df

#This function filters the data set to the specified candidate and survey date
def df_filter(df, candidate, ldate, hdate, state):
    df_cand = df[df.answer==candidate]
    df_cand = df_cand[(df_cand.end_date >= ldate) & (df_cand.end_date <= hdate)]

    if state=='All':
        pass
    else:
        df_cand=df_cand[df_cand.state==state]
        
    return df_cand

#This function calculates the average and weighted average survey percentage
def df_stats(df):
    #Standard Error
    df['ratio']=df['pct']/100
    df['standard_error']=(df['ratio']*(1-df['ratio']))/(df['sample_size'])
    df['standard_error']=df['standard_error'].astype('float')
    df['standard_error']=np.sqrt(df['standard_error'])
    
    #Standard Deviation
    df['standard_deviation']=df['standard_error']*np.sqrt(df['sample_size'])
    
    #Variance
    df['variance']=df['standard_deviation']*df['standard_deviation']
    
    #weighted average
    df['weight']= df['sample_size']/sum(df['sample_size'])
    df['weight_pct'] = df['ratio']*df['weight']*100
    w_avg = sum(df.weight_pct)
    
    #average
    avg=np.mean(df['ratio'])*100
    
    #confidence interval
    avg_var=sum(df.variance)/len(df)
    avg_stdev=np.sqrt(avg_var)
    ci=2*avg_stdev
    
    return df, w_avg, avg, ci

#%%Data Clean
df = df_clean(df)

#%% Overall General Election Percentage
# Trump Percentage
df_trump = df_filter(df, 'Trump', '2020-09-13', '2020-10-13','All')
t_metrics = df_stats(df_trump)

# Biden Percentage
df_biden = df_filter(df, 'Biden', '2020-09-13', '2020-10-13', 'All')
b_metrics = df_stats(df_biden)

# Biden Lead
b_percent=b_metrics[2]
t_percent=t_metrics[2]
other_percent=100-(b_percent + t_percent)
margin=b_metrics[3]
lead=(b_percent-t_percent)
lead_error=(b_percent-margin)-t_percent

if (lead_error - other_percent) > 0:
    outcome = "Biden"
else:
    outcome= "Within Margin"
    
#%% Swing State General Election Percentages
trump_percent = list()
biden_percent = list()
margin = list()
state=['Colorado', 'Arizona', 'Georgia', 'Florida', 'Texas', 'Iowa', 'Michigan', 'Minnesota', 'Nevada', 'North Carolina', 'Ohio', 'Pennsylvania', 'Wisconsin']

for item in state:
    df_trump = df_filter(df, 'Trump', '2020-10-01', '2020-10-13', item)
    t_metrics = df_stats(df_trump)
    trump_percent.append(t_metrics[2])
    
    df_biden = df_filter(df, 'Biden', '2020-10-01', '2020-10-13', item)
    b_metrics = df_stats(df_biden)
    biden_percent.append(b_metrics[2])
    
    margin.append(b_metrics[3])
    
#%% DataFrame of Swing State Polls
state_percents = pd.DataFrame({'State': state, 'Trump': trump_percent, 'Biden': biden_percent, 'Margin': margin})
state_percents['Lead'] = state_percents['Biden']-state_percents['Trump']











