def parse_pws(json_obj):
    stations = json_obj['location']['nearby_weather_stations']['pws']['station']

    temp = []
    for station in stations:
        obj = {
            'Id': station['id'],
            'Neighborhood': station['neighborhood'],
            'Latitude': station['lat'],
            'Longitude': station['lon']
        }
        temp.append(obj)
        break
    return temp

files = get_file_list('/home/jfconavarrete/Documents/Work/Dissertation/spts-uoe/data/raw/pws')
parsed_data = parse_json_files(files, parse_pws)
pwss = pd.DataFrame(list(itertools.chain.from_iterable(parsed_data))).drop_duplicates()
len(pwss)

#############################################################################################

# bounding box for Greater London
min_longitude = -0.489
min_latitude = 51.28
max_longitude = 0.236
max_latitude = 51.686
london_longitude = -0.127722
london_latitude = 51.507981

# personal weather stations
pwss = [('51.473071', '-0.186834'),
        ('51.501074', '-0.194200'),
        ('51.522628', '-0.155533'),
        ('51.485497', '-0.141714'),
        ('51.531606', '-0.112199'),
        ('51.500954', '-0.093199'),
        ('51.523703', '-0.069439'),
        ('51.532167', '-0.030515'),
        ('51.508000', '-0.020387'),
        ('51.507576', '-0.127794')]

stations_map = folium.Map(location=[london_latitude, london_longitude], zoom_start=12,
                          min_lat=min_latitude, max_lat=max_latitude,
                          min_lon=min_longitude, max_lon=max_longitude)

for pws in pwss:
    folium.Marker([pws[0], pws[1]]).add_to(stations_map)

folium.Map.save(stations_map, 'reports/maps/pws_map.html')

stations_map

#############################################################################################


def download(url_string, file_name):
    """Download the given resource to the given file"""

    response = urllib2.urlopen(url_string)
    with open(file_name, "wb") as f:
        f.write(response.read())


path = '/home/jfconavarrete/Documents/Work/Dissertation/spts-uoe/data/raw/weather'
url_template = 'http://api.wunderground.com/api/8494fbcae3235601/history_%s/q/%s,%s.json'
# url_template = 'http://api.wunderground.com/api/8494fbcae3235601/history_%s/q/%s,%s.json'

# iterate through all days and stations
for day in days[-1:]:
    for i, pws in enumerate(pwss):
        url_string = url_template % (day.strftime('%Y%m%d'), pws[0], pws[1])
        file_name = '%s/WEATHER%i-%s.json' % (path, i, day.strftime('%Y-%m-%d'))
        download(url_string, file_name)
    # sleep 60 seconds as the api only allows 10 requests per minute
    time.sleep(61)

#############################################################################################

def get_file_date(file_name):
    """Gets the file's date"""

    file_basename = os.path.basename(file_name)
    idx = file_basename.find('-')
    file_date = file_basename[idx + 1:]
    return datetime.strptime(file_date, '%Y-%m-%d.json')


def pws_id_filter(pws_id):
    def filter_fn(file_name):
        return pws_id == file_name.replace('WEATHER', '').split('-')[0]

    return filter_fn

#############################################################################################

def parse_weather(json_obj):
    """Parses Wunderground API History JSON response"""

    return [parse_observation(element) for element in json_obj['history']['observations']]


def parse_observation(element):
    """Parses a JSON observation object to a dictionary"""

    obj = {
        'date': element['date']['pretty'],
    }

    return obj

    records = parse_dir('/home/jfconavarrete/Documents/Work/Dissertation/spts-uoe/data/raw/weather',
                        parse_weather, filter_fn=pws_id_filter('0'), sort_fn=get_file_date)


pwss = pd.DataFrame(list(itertools.chain.from_iterable(records)))
pwss

##############################################################################################

import math

df = pd.concat([pi24_results.xs((1.0, 'MORNING_PEAK'), level=('Priority', 'PeakHours')), 
               pi24_results.xs((1.0, 'EVENING_PEAK'), level=('Priority', 'PeakHours')),
               pi24_results.xs((1.0, 'NON_PEAK'), level=('Priority', 'PeakHours'))],
               axis=1)
df.columns = ['MorningPeak', 'EveningPeak', 'NonPeak']
#df.EveningPeak = df.EveningPeak - df.MorningPeak
#df.EveningPeak = df.EveningPeak.apply(math.fabs)
df.plot.line()