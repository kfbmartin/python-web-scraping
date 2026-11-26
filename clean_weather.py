import csv
import pandas as pd

# Load the raw weather dataset
df = pd.read_csv("weather_raw.csv")

# Check data types, dimensions, missing values, and for duplicate records
print(df.head())
df.info()
print(df.shape)
print(df.isnull().sum())
print(df.duplicated().sum())

# Remove leading and trailing whitespance from all columns
for column in df.columns:
    df[column] = df[column].str.strip()

# Verify whitespace remove and check for duplicate records
print(df.head())
print(df.duplicated().sum())

# Remove units of measurement from temperature and wind
df['Temperature'] = df['Temperature'].str.replace("°F", "").str.strip()
df['Wind']= df['Wind'].str.replace("mph", "").str.strip()

# Verify units have been removed
print(df.head())
df.info()

# Convert temperature and wind to numeric data types
# Convert invalid or malformed meaurenments to NAN
df['Temperature'] = pd.to_numeric(df['Temperature'],errors="coerce")
df['Wind'] = pd.to_numeric(df['Wind'],errors="coerce")

# Verify cleaned data
print(df.head())
df.info()
print(df.isnull().sum())

# Missing Data Strategy
# Athens is missing wind speed.
# Baghdad and Tehran are missing both temperature and wind speed.
# Retain all 143 city records and leave missing values as NaN.
# Replacing missing values with zero or an average could introduce inaccurate weather measurements into the dataset.

print(df[df['Temperature'].isnull() | df['Wind'].isnull()])

# Rename columns to include the removed units of measurement
df = df.rename(columns={'Temperature': 'Temperature_F', 'Wind':'Wind_mph'})

# Verify the final cleaned dataset
print(df.head())
print(df.columns)
df.info()

# Create temperature categories
bins = [float('-inf'), 32, 50, 65, 80, 90, float('inf')]

labels = ['Freezing', 'Cold', 'Cool', 'Warm', 'Hot', 'Very Hot']

# Create temperature categories
df['Temperature_Category'] = pd.cut(df['Temperature_F'], bins=bins, labels=labels)

# Verify temperature categories
print(df[['City', 'Temperature_F', 'Temperature_Category']].head())

# Count the number of cities in each temperature category
print(df['Temperature_Category'].value_counts(dropna=False))

# Aggregations
average_temp = df['Temperature_F'].mean()
min_temp = df['Temperature_F'].min()
max_temp = df['Temperature_F'].max()
average_wind = df['Wind_mph'].mean()

# Print Weather Aggregations
print("Average Temperature:", round(average_temp, 2))
print("Minimum Temperature:", min_temp)
print("Maximum Temperature:", max_temp)
print("Average Wind Speed:", round(average_wind, 2))

# Average Temperate Group by Country
average_temp_country = df.groupby('Country')['Temperature_F'].mean()
average_wind_country = df.groupby('Country')['Wind_mph'].mean()

print(average_temp_country)
print(average_wind_country)

hottest_city = df[df['Temperature_F'] == max_temp]
coldest_city = df[df['Temperature_F'] == min_temp]
windiest_city = df[df['Wind_mph'] == df['Wind_mph'].max()]
freezing_cities = df[df['Temperature_F'] <= 32]

print("Hottest City:")
print(hottest_city)

print("Coldest City:")
print(coldest_city)

print("Windiest City:")
print(windiest_city)

print("Freezing Cities:")
print(freezing_cities)

print("Number of Freezing Cities:", len(freezing_cities))

# Export the cleaned and transformed weather dataset
df.to_csv("weather_clean.csv", index=False)

# Verify the final dataset dimensions
print("Final Dataset Shape:", df.shape)
print("Cleaned weather data successfully exported.")