import folium
import math

# Example coordinates for Dello Russo locations
locations = [
    {'name': 'New Rochelle', 'lat': 40.897720, 'lon': -73.795080, 'color': 'green'},
    {'name': 'Brooklyn', 'lat': 40.687390, 'lon': -73.985270, 'color': 'blue'},
    {'name': 'Bergenfield', 'lat': 40.927980, 'lon': -73.995780, 'color': 'purple'},
    {'name': 'York Ave', 'lat': 40.779700, 'lon': -73.944590, 'color': 'darkgoldenrod'},
    {'name': 'Iselin', 'lat': 40.564120, 'lon': -74.301360, 'color': 'lightseagreen'},
    {'name': 'Westport', 'lat': 41.1370478, 'lon': -73.3407195, 'color': 'blueviolet'}
]

locationsFuture = [
    {'name': 'Whippany', 'lat': 40.8245442, 'lon': -74.4170972},
    {'name': 'Trenton', 'lat': 40.2203074, 'lon': -74.7659},
    {'name': 'Hartford', 'lat': 41.764582, 'lon': -72.6908547},
    {'name': 'Allentown', 'lat': 40.604873, 'lon': -75.433}
]

locationsPhase3 = [
    {'name': 'Springfield', 'lat': 42.1018764, 'lon': -72.5886727},
    {'name': 'Worcester', 'lat': 42.2625621, 'lon': -71.8018877},
    {'name': 'Boston', 'lat': 42.3554334, 'lon': -71.060511},
    {'name': 'Wayne', 'lat': 40.04555892944336, 'lon': -75.38771057128906},
    {'name': 'Wilmington', 'lat': 39.7459468, 'lon': -75.546589},
    {'name': 'Towson', 'lat': 39.4018513, 'lon': -76.6023803}
]

def create_sector(lat, lon, radius, start_angle, end_angle, num_points=100):
    points = [[lat, lon]]
    for angle in range(start_angle, end_angle + 1):
        angle_rad = math.radians(angle)
        lat_offset = (radius / 111111) * math.cos(angle_rad)  # Approximation for latitude
        lon_offset = (radius / (111111 * math.cos(math.radians(lat)))) * math.sin(angle_rad)  # Approximation for longitude
        points.append([lat + lat_offset, lon + lon_offset])
    points.append([lat, lon])
    return points

# Create a map centered around the first location
map_center = [locations[0]['lat'], locations[0]['lon']]
mymap = folium.Map(location=map_center, zoom_start=10)

# Add circles and markers for each location
for location in locations:
    if location['name'] != 'Bergenfield':
        folium.Circle(
            radius=32186.9,
            location=[location['lat'], location['lon']],
            popup=location['name'],
            color=location['color'],
            fill=True,
            fill_color=location['color'],
            fill_opacity=0.3  # Adjust opacity to reduce overlap visibility
        ).add_to(mymap)
        folium.Marker(
            location=[location['lat'], location['lon']],
            popup=location['name'],
            tooltip=location['name']
        ).add_to(mymap)
    else:
        # Add sector for Bergenfield
        sector_points = create_sector(location['lat'], location['lon'], 32186.9, 300, 420)  # Adjust angles as needed
        folium.Polygon(
            locations=sector_points,
            color=location['color'],
            fill=True,
            fill_color=location['color'],
            fill_opacity=0.3
        ).add_to(mymap)
        folium.Marker(
            location=[location['lat'], location['lon']],
            popup=location['name'],
            tooltip=location['name']
        ).add_to(mymap)

for location in locationsFuture:
    folium.Circle(
        radius=32186.9,
        location=[location['lat'], location['lon']],
        popup=location['name'],
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.3
    ).add_to(mymap)
    folium.Marker(
        location=[location['lat'], location['lon']],
        popup=location['name'],
        tooltip=location['name']
    ).add_to(mymap)

for location in locationsPhase3:
    folium.Circle(
        radius=32186.9,
        location=[location['lat'], location['lon']],
        popup=location['name'],
        color='orange',
        fill=True,
        fill_color='orange',
        fill_opacity=0.3
    ).add_to(mymap)
    folium.Marker(
        location=[location['lat'], location['lon']],
        popup=location['name'],
        tooltip=location['name']
    ).add_to(mymap)

# Adding a legend to the map
legend_html = '''
 <div style="
 position: fixed;
 bottom: 50px;
 left: 50px;
 width: 180px;
 height: 275px;
 border:2px solid grey;
 z-index:9999;
 font-size:14px;
 background-color:white;
 opacity: 0.8;
 ">
 <h4 style="margin:10px;">Legend</h4>
 <i style="background:red; width:10px; height:10px; display:inline-block; margin:5px;"></i> Phase 2 Locations<br>
 <i style="background:orange; width:10px; height:10px; display:inline-block; margin:5px;"></i> Phase 3 Locations<br>
 <i style="background:purple; width:10px; height:10px; display:inline-block; margin:5px;"></i> Bergenfield<br>
 <i style="background:blue; width:10px; height:10px; display:inline-block; margin:5px;"></i> Brooklyn<br>
 <i style="background:lightseagreen; width:10px; height:10px; display:inline-block; margin:5px;"></i> Iselin<br>
 <i style="background:green; width:10px; height:10px; display:inline-block; margin:5px;"></i> New Rochelle<br>
 <i style="background:blueviolet; width:10px; height:10px; display:inline-block; margin:5px;"></i> Westport<br>
 <i style="background:darkgoldenrod; width:10px; height:10px; display:inline-block; margin:5px;"></i> York Avenue<br>
 </div>
'''

mymap.get_root().html.add_child(folium.Element(legend_html))

# Save the map to an HTML file
mymap.save("dello_russo_map_test.html")
