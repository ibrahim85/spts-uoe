import folium

lon_min_longitude = -0.489
lon_min_latitude = 51.28
lon_max_longitude = 0.236
lon_max_latitude = 51.686
lon_center_longitude = -0.127722
lon_center_latitude = 51.507981

def create_london_map():
    return folium.Map(location=[lon_center_latitude, lon_center_longitude], zoom_start=12,
                      min_lat=lon_min_latitude, max_lat=lon_max_latitude,
                      min_lon=lon_min_longitude, max_lon=lon_max_longitude)


def draw_stations_map(stations_df, create_marker, london_map=None):
    if london_map is None:
        london_map = create_london_map()

    for index, station in stations_df.iterrows():
        create_marker(station).add_to(london_map)

    return london_map

