import logging
import uuid

from datetime import datetime
    
global_start = datetime(2016,5,16)
global_end = datetime(2016,6,26)

def day_range(start, hours=None, fullday=False, daylight=False):
    if fullday:
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start.replace(hour=23, minute=59, second=59, microsecond=999)
        return start, end
        
    if hours is not None:
        end = start + timedelta(hours=hours)
        return start, end
    
    if daylight:
        start = start.replace(hour=7, minute=0, second=0, microsecond=0)
        end = start.replace(hour=21, minute=59, second=59, microsecond=999)
        return start, end

def filter_by_time(df, start, end):
    timestamp = df['Timestamp']
    selector = (timestamp >= start) & (timestamp <= end)
    return df[selector]
    
def filter_by_id(df, idval):
    return df[df['Id'] == idval]


def find_next(df, start_loc):
    if start_loc + 1 == len(df):
        return None
    else:    
        return df.loc[start_loc + 1]
    
def get_periods(start, end):
    if (end.date() - start.date()).days > 0:
        return True, start.replace(hour=23, minute=59, second=59), (start + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        return False, end, None

def find_zero_periods_of(station_id, df, col_name):
    df = filter_by_id(df, station_id).copy().reset_index()

    entries = []
    for idx in df[df[col_name] == 0].index:
        next_reading = find_next(df, idx, col_name)
        if next_reading is None:
            continue
            
        start, end = df.loc[idx]['Timestamp'], next_reading['Timestamp']                
        periodId = uuid.uuid4()
        
        distinct_days = True
        while distinct_days:
            distinct_days, current_end, next_start = get_periods(start, end)
            
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

def find_zero_periods(df, col_name):
    periods = []
    [periods.append(find_zero_periods_of(station_id, df, col_name)) for station_id in df['Id'].unique()]
    return pd.DataFrame(list(itertools.chain.from_iterable(periods))) 

def group_ellapsed(df):
    ellapsed = lambda x: np.round((x[-1] - x[0]) / pd.np.timedelta64(1, 'm'))
    
    collapsed = df.groupby(['Id', 'PeriodId']).aggregate(lambda x: tuple(x))
    collapsed['Ellapsed'] = collapsed['Timestamp'].apply(ellapsed)
    collapsed.reset_index(level=0, inplace=True)
    collapsed.reset_index(level=0, inplace=True)
    
    return collapsed

def add_station_info(df):
    df_stations = df.merge(stations, on='Id', how='inner')
    df_stations.drop(['TerminalName','PlaceType','Installed','Temporary','Locked','RemovalDate','InstallDate','ShortName'], axis=1, inplace=True)
    return df_stations