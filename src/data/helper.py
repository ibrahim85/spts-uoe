import logging

from datetime import datetime
from matplotlib.ticker import FuncFormatter
    
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
    
def add_station_info(df, stations, cols=None):
    df_stations = df.merge(stations, on='Id', how='left')
    if cols is None:
        df_stations.drop(['TerminalName','PlaceType','Installed','Temporary','Locked','RemovalDate','InstallDate','ShortName'], axis=1, inplace=True)
    else:
        to_drop = set(stations.columns) - set(['Priority'])
        df_stations.drop(to_drop, axis=1, inplace=True)
    return df_stations

epoch_formatter = FuncFormatter(lambda x, pos: datetime.fromtimestamp(x).timestamp.strftime("%H:%M"))