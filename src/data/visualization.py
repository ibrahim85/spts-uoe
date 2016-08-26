import folium
import matplotlib.colors as clrs

from palettable.colorbrewer.sequential import Oranges_9
from palettable.colorbrewer.qualitative import Dark2_7

lon_min_longitude = -0.489
lon_min_latitude = 51.28
lon_max_longitude = 0.236
lon_max_latitude = 51.686
lon_center_longitude = -0.127722
lon_center_latitude = 51.507981

def map_priority_color(priority):
    if priority == 1:
        return '#ff1a1a', '#cc0000'
    elif priority == 2:
        return '#3333ff', '#0000cc'
    else: 
        return '#ffff1a', '#b3b300'

def create_london_map():
    londonmap = folium.Map(location=[lon_center_latitude, lon_center_longitude], zoom_start=12,
                      min_lat=lon_min_latitude, max_lat=lon_max_latitude,
                      min_lon=lon_min_longitude, max_lon=lon_max_longitude)
    folium.TileLayer('stamentoner').add_to(londonmap)
    return londonmap


def draw_stations_map(stations_df, create_marker, london_map=None):
    if london_map is None:
        london_map = create_london_map()

    for index, station in stations_df.iterrows():
        create_marker(station).add_to(london_map)

    return london_map

def cmap_to_hex(cmap, value):
    if isinstance(cmap, list):
        rgb = cmap[int(value)]    
    else:
        rgb = cmap(value)[:3]
    return clrs.rgb2hex(rgb)
    
def create_result_marker(col_name):
    def create_marker(station):
        line_color = map_priority_color(station['Priority'])[1]
        fill_color = cmap_to_hex(Oranges_9.mpl_colormap, station[col_name])
    
        label = "%s - %f" % (station['Name'], station['GAM'])

        return folium.CircleMarker(location=[station['Latitude'], station['Longitude']], radius=100,
                        popup=label, color=line_color, fill_color=fill_color, fill_opacity=0.9)
    
    return create_marker
    
def create_cluster_marker(col_name):
    def create_marker(station):
        line_color = cmap_to_hex(Dark2_7.mpl_colors, station[col_name])
        fill_color = cmap_to_hex(Dark2_7.mpl_colors, station[col_name])
    
        label = "%s - %f" % ('Id', station[col_name])

        return folium.CircleMarker(location=[station['Latitude'], station['Longitude']], radius=100,
                        popup=label, color=line_color, fill_color=fill_color, fill_opacity=0.9)
    
    return create_marker