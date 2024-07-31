import pandas as pd
import folium
from folium.plugins import HeatMap
from opencage.geocoder import OpenCageGeocode
import logging

logging.basicConfig(level=logging.INFO)
def geocode_zipcode(zipcode, geocoder):
    try:
        zipcode = zipcode.zfill(5)
        result = geocoder.geocode(zipcode, countrycode='us')
        if result and len(result):
            logging.info(f"Geocoded {zipcode}: {result[0]['geometry']}")
            return [result[0]['geometry']['lat'], result[0]['geometry']['lng']]
        else:
            logging.warning(f"No results for {zipcode}")
    except Exception as e:
        logging.error(f"Error geocoding {zipcode}: {e}")
        return None
    return None

df = pd.read_csv('/Users/elimichuda/Desktop/SURG2124.CSV', encoding='ISO-8859-1', dtype={'PatZip': str}, low_memory=False)

print(df.columns)


df = df.head(2450)

key = '41a1e221e9944a4baf351a41e9683644'
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
