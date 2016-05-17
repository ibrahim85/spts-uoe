import pandas as pd
import itertools
from parse_json import parse_dir, parse_cycles

records = parse_dir('/home/jfconavarrete/Documents/Work/Dissertation/spts-uoe/data/dev', parse_cycles)

dataset = pd.DataFrame(list(itertools.chain.from_iterable(records)))

# convert columns to their appropriate datatypes
dataset['InstallDate'] = pd.to_numeric(dataset['InstallDate'], errors='raise')
dataset['Installed'] = dataset['Installed'].astype('bool_')
dataset['Locked'] = dataset['Locked'].astype('bool_')
dataset['NbNikes'] = dataset['NbBikes'].astype('uint16')


# convert timestamp to datetime
dataset['Timestamp'] =  pd.to_datetime(dataset['Timestamp'], format='%Y-%m-%dT%H:%M:%S.%f')
dataset['InstallDate'] = pd.to_datetime(dataset['InstallDate'], unit='ms')

print dataset.info()

#print dataset.describe(include='all')


