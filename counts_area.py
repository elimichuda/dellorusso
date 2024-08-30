import pandas as pd
from opencage.geocoder import OpenCageGeocode

key = '047040cb241e47d4a12287c7e2e16fe3'
geocoder = OpenCageGeocode(key)

# Load the dataset
df = pd.read_csv('/Users/elimichuda/Desktop/SURG2124.CSV', encoding='ISO-8859-1', dtype={'PatZip': str}, low_memory=False)
df = df.iloc[11740:]

# Function to geocode ZIP codes
def geocode_zipcode(zipcode, geocoder):
    try:
        zipcode = zipcode.zfill(5)  # Ensure ZIP code has 5 digits
        result = geocoder.geocode(zipcode, countrycode='us')
        if result and len(result):
            return [result[0]['geometry']['lat'], result[0]['geometry']['lng']]
    except Exception as e:
        print(f"Error geocoding {zipcode}: {e}")
    return None

df['coords'] = df['PatZip'].apply(lambda x: geocode_zipcode(x, geocoder))
df = df.dropna(subset=['coords'])  # Drop rows where geocoding failed
df['latitude'] = df['coords'].apply(lambda x: x[0])
df['longitude'] = df['coords'].apply(lambda x: x[1])

regions = {
    "red": [(40.7433066, -74.0323752), (40.384263,-74.089879), (40.1728871,-74.9926688), (40.9831598, -74.9602972)], #Hoboken, Middletown Township, Holland, Blairstown
    "blue": [(41.0003754, -73.9304141), (40.7433066, -74.0323752), (40.9831598, -74.9602972), (41.3750937, -74.692663)], #Rockleigh, Hoboken, Blairstown, Port Jervis
    "brown": [(41.0003754, -73.9304141), (41.3750937, -74.692663), (41.289811,-73.9204922), (41.289811,-73.9204922)], #Rockleigh, Port Jervis, Peekskill, PeekSkill
    "pink": [(41.289811,-73.9204922), (41.0003754, -73.9304141), (41.03228933987469,-73.62919825567162), (41.3082138,-72.9250518)], #Peekskill, Rockleigh, Greenwich, New Haven
    "yellow": [(41.0003754, -73.9304141), (40.7433066, -74.0323752), (40.7017103,-74.0131489), (40.7108086,-73.9774597), (41.03228933987469,-73.62919825567162)], #Rockleigh, Hoboken, South Ferry, Corlear's Hook, Greenwich
    "orange": [(40.7017103,-74.0131489), (40.7108086,-73.9774597),  (40.9105988,-73.5620864), (41.09869607445502,-72.3688044276851), (41.043731924732434,-71.9170784192819), (40.85234625752942,-72.44379451603675), (40.6956552,-73.3256753), (40.593172302989544,-73.75291157782338)], #South Ferry, Corlear's Hook, Bayville, Babylon
    "green": [(40.7017103,-74.0131489), (40.645404309462855,-73.87338227634207), (40.58391915008468,-73.8776759681395), (40.570055664357604,-73.99733579684487), (40.630895052342055,-74.04202711131802)] #South Ferry, Shirley Chisalm, Shore Blvd,
}


def is_inside_region(point, region_bounds):
    lat, lon = point
    lat_min = min([b[0] for b in region_bounds])
    lat_max = max([b[0] for b in region_bounds])
    lon_min = min([b[1] for b in region_bounds])
    lon_max = max([b[1] for b in region_bounds])
    return lat_min <= lat <= lat_max and lon_min <= lon <= lon_max

# Function to assign regions to each patient based on their coordinates
def assign_region(row):
    point = (row['latitude'], row['longitude'])
    for region_name, bounds in regions.items():
        if is_inside_region(point, bounds):
            return region_name
    return "unknown"

# Assign each patient to a region
df['region'] = df.apply(assign_region, axis=1)

# Count the number of patients in each region
patient_counts = df['region'].value_counts()

# Display the counts for each region
print(patient_counts)


