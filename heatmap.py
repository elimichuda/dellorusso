import os
import pandas as pd
import folium
from folium.plugins import HeatMap
from opencage.geocoder import OpenCageGeocode

def geocode_zipcode(zipcode, geocoder):
    try:
        zipcode = zipcode.zfill(5)
        result = geocoder.geocode(zipcode, countrycode='us')
        if result and len(result):
            return [result[0]['geometry']['lat'], result[0]['geometry']['lng']]
    except Exception as e:
        print(f"Error geocoding {zipcode}: {e}")
        return None  # Handle invalid or missing zipcodes
    return None

# Load the dataset
df = pd.read_csv('/Users/elimichuda/Desktop/SURG2124.CSV', encoding='ISO-8859-1', dtype={'PatZip': str}, low_memory=False)
# Print the columns to check the data
print(df.columns)

# Set API key for geocoding
key = '047040cb241e47d4a12287c7e2e16fe3'
geocoder = OpenCageGeocode(key)

# Function to create heat map
def create_heat_map(data, year):
    data['coords'] = data['PatZip'].apply(lambda x: geocode_zipcode(x, geocoder))
    data = data.dropna(subset=['coords'])
    data['latitude'] = data['coords'].apply(lambda x: x[0])
    data['longitude'] = data['coords'].apply(lambda x: x[1])
    heat_data = data[['latitude', 'longitude']].values.tolist()
    map_center = [data['latitude'].mean(), data['longitude'].mean()]
    mymap = folium.Map(location=map_center, zoom_start=10)
    HeatMap(heat_data).add_to(mymap)
    map_filename = f"patients_heatmap_{year}.html"
    mymap.save(map_filename)
    print(f"Saved heat map for {year} as {map_filename}")

# Create heat maps for each year
create_heat_map(df.iloc[0:4558], 2021)
create_heat_map(df.iloc[4558:8091], 2022)
create_heat_map(df.iloc[8091:11740], 2023)
create_heat_map(df.iloc[11740:], 2024)

