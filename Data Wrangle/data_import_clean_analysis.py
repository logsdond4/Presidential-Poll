# -*- coding: utf-8 -*-
"""
Author: Dan Logsdon
Date: 10/09/2020

This code uses open source data obtained from:
https://github.com/fivethirtyeight/data/tree/master/polls

This file calculates the weighted percentage score for each candidate for the general election
and calculates the overall candidate lead percentage.

"""

## Package Import
import pandas as pd
import os

## Import Data
root = os.path.dirname(os.path.dirname(__file__)) #root folder
src = root + '\\src' #source folder
file = src + '\\president_polls.csv' #input file
df=pd.read_csv(file)

## Functions
# This function cleans the dataset (e.g., removing NA values, data conversion)
def df_clean(df): 
    df['end_date'] = pd.to_datetime(df['end_date'])
    df = df[df['sample_size'].notna()]
    return df

#This function filters the data set to the specified candidate and survey date
def df_filter(df, candidate, ldate, hdate):
    df_cand = df[df.answer==candidate]
    df_cand = df_cand[(df_cand.end_date >= ldate) & (df_cand.end_date <= hdate)]
    return df_cand

#This function calculates the weighted average survey percentage
def df_calc(df):
    df['weight']= df['sample_size']/sum(df['sample_size'])
    df['weight_pct'] = df['pct']*df['weight']
    pct = sum(df.weight_pct)
    return pct

## Data Clean
df = df_clean(df)

## Trump Percentage
df_trump = df_filter(df, 'Trump', '2020-09-08', '2020-10-08')
trump_percent = df_calc(df_trump)

## Biden Percentage
df_biden = df_filter(df, 'Biden', '2020-09-08', '2020-10-08')
biden_percent = df_calc(df_biden)

## Biden Lead
lead=biden_percent-trump_percent




