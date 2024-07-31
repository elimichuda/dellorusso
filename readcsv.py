import pandas as pd

# Read the CSV file with a specified encoding
df = pd.read_csv('/Users/elimichuda/Desktop/SURG2124.CSV', encoding='ISO-8859-1', low_memory=False)

# Print the column names to find the correct column for zip codes
print(df.columns)
# Check the first few entries of the 'PatZip' column
print(df['PatZip'].head())

# Check for any null values in the 'PatZip' column
print(df['PatZip'].isnull().sum())

