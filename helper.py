import pandas as pd
import numpy as np

df=pd.read_csv('clean_dataset.csv')

def group_by_year(dataframe, year):
    global df
    grouped_df = dataframe.groupby('season')
    year_df = grouped_df.get_group(year)
    return year_df
