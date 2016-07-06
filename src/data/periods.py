import logging
import itertools
import uuid

import pandas as pd
import numpy as np

from datetime import datetime, timedelta
from helper import filter_by_id, filter_by_time

morning_peaktime_start = lambda timestamp: timestamp.replace(hour=7, minute=0, second=0, microsecond=0)
morning_peaktime_end = lambda timestamp: timestamp.replace(hour=10, minute=0, second=0, microsecond=0)
evening_peaktime_start = lambda timestamp: timestamp.replace(hour=16, minute=0, second=0, microsecond=0)
evening_peaktime_end = lambda timestamp: timestamp.replace(hour=19, minute=0, second=0, microsecond=0)

def find_next(df, start_loc):
    if start_loc + 1 == len(df):
        return None
    else:    
        return df.loc[start_loc + 1]
            
def get_periods(start, end):
    current_end = None
    next_start = None
    
    # check if the dates are in two different days
    if are_different_days(start, end):
        if start > evening_peaktime_end(start):
            current_end = start.replace(hour=23, minute=59, second=59, microsecond=999999)
            next_start = (start + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            return True, current_end, next_start
            
        
    # check if the start or end are fall between peak times
    is_start_peaktime, start_time = is_peaktime(start)
    is_end_peaktime, end_time = is_peaktime(end)
    if is_start_peaktime & (not is_end_peaktime):
        current_end = morning_peaktime_end(start) if start_time == 'MORNING_PEAK' else evening_peaktime_end(start)
        next_start = current_end + timedelta(minutes=1)
        return True, current_end, next_start
    if (not is_start_peaktime) & is_end_peaktime:        
        next_start = morning_peaktime_start(end) if end_time == 'MORNING_PEAK' else evening_peaktime_start(end)
        current_end = next_start - timedelta(minutes=1)
        return True, current_end, next_start
    if is_start_peaktime & is_end_peaktime & (start_time != end_time):
        current_end = morning_peaktime_end(start)
        next_start = current_end + timedelta(minutes=1)
        return True, current_end, next_start
        
    # check if start and end enclose peak times
    if (start < morning_peaktime_start(start)) & (end > morning_peaktime_end(end)):        
        current_end = morning_peaktime_start(start) - timedelta(minutes=1)
        next_start = morning_peaktime_start(start)
        return True, current_end, next_start
    if (start < evening_peaktime_start(start)) & (evening_peaktime_end(end) < end):        
        current_end = evening_peaktime_start(start) - timedelta(minutes=1)
        next_start = evening_peaktime_start(start)
        return True, current_end, next_start
        
    return False, end, None    

def are_different_days(start, end):
    return (end.date() - start.date()).days > 0

def is_peaktime(timestamp):    
    if (timestamp >= morning_peaktime_start(timestamp)) & (timestamp <= morning_peaktime_end(timestamp)):
        return True, 'MORNING_PEAK'
        
    if (timestamp >= evening_peaktime_start(timestamp)) & (timestamp <= evening_peaktime_end(timestamp)):
        return True, 'EVENING_PEAK'
    
    return False, 'NON-PEAK'

def find_zero_periods_of(station_id, df, col_name, group=False):
    df = filter_by_id(df, station_id).copy().reset_index()

    entries = []
    for idx in df[df[col_name] == 0].index:
        next_reading = find_next(df, idx)
        if next_reading is None:
            continue
            
        start, end = df.loc[idx]['Timestamp'], next_reading['Timestamp']                
        periodId = uuid.uuid4()
        
        distinct_days = True
        while distinct_days:
            distinct_days, current_end, next_start = get_periods(start, end)
            
            if not group:
                periodId = uuid.uuid4() 
            
            # create entries
            entries.append({
                'Id': station_id,
                'Timestamp': start,
                'PeriodId': periodId
            })
        
            entries.append({
                'Id': station_id,
                'Timestamp': current_end,
                'PeriodId': periodId
            })
            
            start = next_start        
        
    return entries

def find_zero_periods(df, col_name, group=False):
    periods = []
    [periods.append(find_zero_periods_of(station_id, df, col_name, group)) for station_id in df['Id'].unique()]
    return pd.DataFrame(list(itertools.chain.from_iterable(periods))) 

def group_ellapsed(df):
    ellapsed = lambda x: np.round((x[-1] - x[0]) / pd.np.timedelta64(1, 'm'))
    
    collapsed = df.groupby(['Id', 'PeriodId']).aggregate(lambda x: tuple(x))
    collapsed['Ellapsed'] = collapsed['Timestamp'].apply(ellapsed)
    collapsed.reset_index(level=0, inplace=True)
    collapsed.reset_index(level=0, inplace=True)
    
    collapsed.rename(columns={'Timestamp': 'Period'}, inplace=True)
    
    return collapsed
    
def get_period_day(period):
    start = period[0]
    for entry in period:
        if are_different_days(start, entry):
            raise ValueError('Different days in period')
    return start.date()
    
def get_peak_hours(period):
    start = period[0]
    for entry in period:
        if is_peaktime(start)[1] != is_peaktime(entry)[1]:
            raise ValueError('Different times in period %s != %s' % (start, entry))
    return is_peaktime(start)[1]