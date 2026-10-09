import pandas as pd

dfBlocks = pd.read_csv('GeoLite2-City-CSV_20261006/GeoLite2-City-Blocks-IPv4.csv', dtype='string')
dfLocation = pd.read_csv('GeoLite2-City-CSV_20261006/GeoLite2-City-Locations-en.csv',  dtype='string')

print("rows in block file: " + str(len(dfBlocks)))
print("rows in location file: " + str(len(dfLocation)))
print(dfBlocks.columns)
print(dfLocation.columns)
print("unique geoname_ids in block file: " + str(len(dfBlocks['geoname_id'].unique())))

# the number of blocks records with a valid geoname_id
print("rows in block file with valid geoname_id: " + str(len(dfBlocks[dfBlocks['geoname_id'] != 0])))

# the number of unique geoname_id values in the locations
print("unique geoname_ids in location file: " + str(len(dfLocation['geoname_id'].unique())))

df = pd.merge(dfBlocks, dfLocation, on=['geoname_id'])

print("len merged df: " + str(len(df)))
print("unique geoname_ids in merged df: " + str(len(df['geoname_id'].unique())))

#print(dfBlocks.head())
#print(dfLocation.head())

# there's 1 geoname_id in blocks that's not in locations
set_a, set_b = set(dfBlocks['geoname_id']), set(dfLocation['geoname_id'])
print("geoname_ids in blocks but not locations: " + str(len(set_a - set_b)))

# there are 3659784 blocks with an associated location, how many of those have lat long
valid_rows = df[(df['latitude'] != 0) & (df['longitude'] != 0)]
print("rows with valid lat long: " + str(len(valid_rows)))
# there were 3659784 rows with valid lat long, so that is always set

invalid_records = dfBlocks[dfBlocks['geoname_id'].isna()]
#invalid_records.to_csv('invalid_blocks.csv')
print(f"records with no geoname_id: {len(invalid_records)}")

# there are no invalid records without a registered_country_geoname_id
print(len(invalid_records[invalid_records['registered_country_geoname_id'].isna()]))

found_count = invalid_records['registered_country_geoname_id'].isin(dfLocation['geoname_id']).sum()
print(f"registered_country_geoname_ids found in location dataframe: {found_count}")

# number of locations with that havea city set
print(f"locations with a city: {len(dfLocation[dfLocation['city_name'].notna()])}")
print(f"locations with a subdivision1: {len(dfLocation[dfLocation['subdivision_1_name'].notna()])}")
print(f"locations with a subdivision2: {len(dfLocation[dfLocation['subdivision_2_name'].notna()])}")
print(f"locations with a country name: {len(dfLocation[dfLocation['country_name'].notna()])}")
print(f"locations with a country code: {len(dfLocation[dfLocation['country_iso_code'].notna()])}")

# list of locations that have a country name but not a country code
locations_without_country_code = dfLocation[
    dfLocation['country_name'].notna() &
    dfLocation['country_iso_code'].isna()
]
print(locations_without_country_code)
locations_without_country_code.to_csv('locations_without_country_code.csv')

# print all the count of all cities
print(f"locations with a city: {len(dfLocation[dfLocation['city_name'].notna()])}")

# print the count of cities where a country is not also specified
print(f"locations with a city and no country: {len(dfLocation[dfLocation['city_name'].notna() & dfLocation['country_name'].isna()])}")

# print all the count of subdivision_1_name, and the count of the subdivision_1_name where the country is not specified
print(f"locations with a subdivision_1_name: {len(dfLocation[dfLocation['subdivision_1_name'].notna()])}")
print(f"locations with a subdivision_1_name and no country: {len(dfLocation[dfLocation['subdivision_1_name'].notna() & dfLocation['country_name'].isna()])}")

# print all the count of subdivision_2_name, and the count of the subdivision_2_name where the country is not specified
print(f"locations with a subdivision_2_name: {len(dfLocation[dfLocation['subdivision_2_name'].notna()])}")
print(f"locations with a subdivision_2_name and no country: {len(dfLocation[dfLocation['subdivision_2_name'].notna() & dfLocation['country_name'].isna()])}")

# print all the count of subdivision_2_name where subdivision_1_name is also specified
print(f"locations with a subdivision_2_name and a subdivision_1_name: {len(dfLocation[dfLocation['subdivision_2_name'].notna() & dfLocation['subdivision_1_name'].notna()])}")

# conversely, print the count of subdivison_1_name where subdivision_2_name is not specified
print(f"locations with a subdivision_1_name and no subdivision_2_name: {len(dfLocation[dfLocation['subdivision_1_name'].notna() & dfLocation['subdivision_2_name'].isna()])}")

# print the count of subdivision_2_name where subdivision_1_name is not specified
print(f"locations with a subdivision_2_name and no subdivision_1_name: {len(dfLocation[dfLocation['subdivision_2_name'].notna() & dfLocation['subdivision_1_name'].isna()])}")

# print the count of city_name where one or both of subdivision_1_name and subdivision_2_name are not specified
print(f"locations with a city_name and no subdivision_1_name or subdivision_2_name: {len(dfLocation[dfLocation['city_name'].notna() & (dfLocation['subdivision_1_name'].isna() | dfLocation['subdivision_2_name'].isna())])}")

# print the count where continent_name is not set but any other datapoint is:
print(f"locations with no continent_name, but some more specific *_name: {len(dfLocation[dfLocation['continent_name'].isna() & (dfLocation['city_name'].notna() | dfLocation['subdivision_1_name'].notna() | dfLocation['subdivision_2_name'].notna() | dfLocation['country_name'].notna())])}")

# print the count of geoname_id where no continent is set
print(f"locations with no continent_name: {len(dfLocation[dfLocation['continent_name'].isna()])}")