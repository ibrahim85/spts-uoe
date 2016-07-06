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
day_time_end = lambda timestamp: timestamp.replace(hour=23, minute=59, second=59, microsecond=999999)

def find_next(df, start_loc):
    if start_loc + 1 == len(df):
        return None
    else:    
        return df.loc[start_loc + 1]
            
def get_periods(start, end):
    current_end = None
    next_start = None
    
    splits = np.array([morning_peaktime_start(start), 
              morning_peaktime_end(start), 
              evening_peaktime_start(start), 
              evening_peaktime_end(start), 
              day_time_end(start)])
              
    start_split = next_split(splits, start)
    end_split = next_split(splits, end)
    
    if start_split == end_split:
        return False, end, None
    else:
        current_end = start_split
        next_start = current_end if end_split is not None else current_end + timedelta(microseconds=1)
        return True, current_end, next_start
    
def next_split(splits, timestamp):
    for split_time in splits:
        if timestamp < split_time:
            return split_time            

def are_different_days(start, end):
    return (end.date() - start.date()).days > 0

def is_peaktime(period):    
    start = period[0]
    end = period[-1]
    if (start >= morning_peaktime_start(start)) & (end <= morning_peaktime_end(end)):
        return True, 'MORNING_PEAK'
        
    if (start >= evening_peaktime_start(start)) & (end <= evening_peaktime_end(end)):
        return True, 'EVENING_PEAK'
    
    return False, 'NON-PEAK'

def find_zero_periods_of(station_id, df, col_name):
    df = filter_by_id(df, station_id).copy().reset_index()

    entries = []
    for idx in df[df[col_name] == 0].index:
        next_reading = find_next(df, idx)
        if next_reading is None:
            continue
            
        start, end = df.loc[idx]['Timestamp'], next_reading['Timestamp']                
        group_id = uuid.uuid4()
        
        distinct_days = True
        while distinct_days:
            distinct_days, current_end, next_start = get_periods(start, end)
            
            period_id = uuid.uuid4() 
            
            # create entries
            entries.append({
                'Id': station_id,
                'Timestamp': start,
                'PeriodId': period_id,
                'GroupId': group_id
            })
        
            entries.append({
                'Id': station_id,
                'Timestamp': current_end,
                'PeriodId': period_id,
                'GroupId': group_id
            })
            
            start = next_start        
        
    return entries

def find_zero_periods(df, col_name):
    periods = []
    [periods.append(find_zero_periods_of(station_id, df, col_name)) for station_id in df['Id'].unique()]
    return pd.DataFrame(list(itertools.chain.from_iterable(periods))) 

def get_ellapsed_time(df, by='GroupId'):
    ellapsed = lambda x: np.round((x[-1] - x[0]) / pd.np.timedelta64(1, 'm'))
    
    collapsed = df.groupby(['Id', by]).aggregate(lambda x: tuple(x))
    collapsed['Ellapsed'] = collapsed['Timestamp'].apply(ellapsed)
    collapsed.reset_index(level=0, inplace=True)
    collapsed.reset_index(level=0, inplace=True)
    
    collapsed.rename(columns={'Timestamp': 'Period'}, inplace=True)
    
    if by == 'GroupId':
        collapsed['Period'] = collapsed['Period'].apply(lambda x: (x[0], x[-1]))
    
    return collapsed
    
def get_period_day(period):
    start = period[0]
    for entry in period:
        if are_different_days(start, entry):
            raise ValueError('Different days in period')
    return start.date()

#######################################################
    
import unittest

class PeriodsTest(unittest.TestCase):
    
    #@unittest.skip        
    def test_run(self):
        start = datetime(2016,6,12, 6, 45)
        end = datetime(2016,6,14, 3, 45)
        
        distinct_days = True
        while distinct_days:
            distinct_days, current_end, next_start = get_periods(start, end)
            print start, current_end
            start = next_start   
            
    def test_bothnonpeak_close(self):
        start = datetime(2016,6,13, 5, 45)
        end = datetime(2016,6,14, 6, 45)
        
        cont,current_end, next_start = get_periods(start, end)
        self.assertFalse(cont)
        self.assertEqual(current_end, end)
        self.assertEqual(next_start)
            
    def test_bothnonpeak_close(self):
        start = datetime(2016,6,13, 5, 45)
        end = datetime(2016,6,13, 6, 45)
        
        cont,current_end, next_start = get_periods(start, end)
        self.assertFalse(cont)
        self.assertEqual(current_end, end)
        self.assertIsNone(next_start)
        
    def test_bothnonpeak_apart(self):
        start = datetime(2016,6,13, 5, 45)
        end = datetime(2016,6,13, 11, 45)
        
        cont,current_end, next_start = get_periods(start, end)
        self.assertTrue(cont)
        self.assertEqual(current_end, morning_peaktime_start(start))
        self.assertEqual(next_start, morning_peaktime_start(start))
    
    def test_start_nonpeak_endpeak(self):
        start = datetime(2016,6,13, 5, 45)
        end = datetime(2016,6,13, 7, 45)
        
        cont,current_end, next_start = get_periods(start, end)
        self.assertTrue(cont)
        self.assertEqual(current_end, morning_peaktime_start(start))
        self.assertEqual(next_start, morning_peaktime_start(start))
        
    def test_startpeak_endpeak(self):
        start = datetime(2016,6,13, 7, 45)
        end = datetime(2016,6,13, 8, 45)
        
        cont,current_end, next_start = get_periods(start, end)
        self.assertFalse(cont)
        self.assertEqual(current_end, end)
        self.assertIsNone(next_start)
        
    def test_startpeak_endnonpeak(self):
        start = datetime(2016,6,13, 9, 45)
        end = datetime(2016,6,13, 10, 45)
        
        cont,current_end, next_start = get_periods(start, end)
        self.assertTrue(cont)
        self.assertEqual(current_end, morning_peaktime_end(start))
        self.assertEqual(next_start, morning_peaktime_end(start))
    
#if __name__ == '__main__':
#    unittest.main()