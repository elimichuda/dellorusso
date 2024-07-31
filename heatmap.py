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


df = pd.read_csv('/Users/elimichuda/Desktop/SURG2124.CSV', encoding='ISO-8859-1', dtype={'PatZip': str}, low_memory=False)


print(df.columns)


df = df.head(2450)


key = os.getenv('OPENCAGE_API_KEY')
geocoder = OpenCageGeocode(key)


df['coords'] = df['PatZip'].apply(lambda x: geocode_zipcode(x, geocoder))


df = df.dropna(subset=['coords'])
df['latitude'] = df['coords'].apply(lambda x: x[0])
df['longitude'] = df['coords'].apply(lambda x: x[1])


heat_data = df[['latitude', 'longitude']].values.tolist()


map_center = [df['latitude'].mean(), df['longitude'].mean()]
mymap = folium.Map(location=map_center, zoom_start=10)


HeatMap(heat_data).add_to(mymap)


mymap.save("patients_heatmap.html")
