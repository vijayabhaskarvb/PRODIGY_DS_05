import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

# Load the dataset
dataset = pd.read_csv('SampleData.csv', low_memory=False)
dataset['Accident_Index'] = dataset['Accident_Index'].astype(str)  # Convert to string

# Remove unnecessary columns
dataset.drop(columns=["Unnamed: 0", "Accident_Index", "Police_Force", "Local_Authority_(Highway)", "LSOA_of_Accident_Location"], inplace=True)

# Convert date and time columns to datetime format
dataset["Date"] = pd.to_datetime(dataset["Date"], dayfirst=True)
dataset["Hour"] = pd.to_datetime(dataset["Time"], format='%H:%M', errors='coerce').dt.hour  # Extract hour

dataset.drop(columns=["Time"], inplace=True)  # Time column no longer needed

# Handle missing values correctly
for col in dataset.select_dtypes(include=['number']).columns:
    dataset[col] = dataset[col].fillna(dataset[col].median())  # Fill numeric NaN with median
for col in dataset.select_dtypes(include=['object']).columns:
    dataset[col] = dataset[col].fillna("Unknown")  # Fill categorical NaN with "Unknown"

# Convert Latitude and Longitude to numeric
dataset["Latitude"] = pd.to_numeric(dataset["Latitude"], errors='coerce')
dataset["Longitude"] = pd.to_numeric(dataset["Longitude"], errors='coerce')

# Drop rows where Latitude or Longitude is missing
dataset.dropna(subset=["Latitude", "Longitude"], inplace=True)

# Plot accident distribution by time of day
plt.figure(figsize=(10, 5))
sns.countplot(x=dataset['Hour'], hue=dataset['Hour'], palette='coolwarm', legend=False)
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Accidents")
plt.title("Accident Frequency by Time of Day")
plt.tight_layout()
plt.show()

# Plot accident frequency by day of the week
plt.figure(figsize=(10, 5))
sns.countplot(x=dataset['Day_of_Week'], hue=dataset['Day_of_Week'], palette='viridis', legend=False)
plt.xlabel("Day of the Week")
plt.ylabel("Number of Accidents")
plt.title("Accident Frequency by Day of the Week")
plt.xticks(ticks=range(7), labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
plt.tight_layout()
plt.show()

# Analyze accident severity distribution
plt.figure(figsize=(8, 5))
sns.countplot(x=dataset['Accident_Severity'], hue=dataset['Accident_Severity'], palette='magma', legend=False)
plt.xlabel("Accident Severity (1 = Most Severe, 3 = Least Severe)")
plt.ylabel("Count")
plt.title("Distribution of Accident Severity")
plt.tight_layout()
plt.show()

# Analyze weather conditions impact
plt.figure(figsize=(12, 5))
sns.countplot(y=dataset['Weather_Conditions'], hue=dataset['Weather_Conditions'], palette='Set2', order=dataset['Weather_Conditions'].value_counts().index, legend=False)
plt.xlabel("Number of Accidents")
plt.ylabel("Weather Conditions")
plt.title("Impact of Weather Conditions on Accidents")
plt.tight_layout()
plt.show()

# Analyze road surface conditions impact
plt.figure(figsize=(12, 5))
sns.countplot(y=dataset['Road_Surface_Conditions'], hue=dataset['Road_Surface_Conditions'], palette='coolwarm', order=dataset['Road_Surface_Conditions'].value_counts().index, legend=False)
plt.xlabel("Number of Accidents")
plt.ylabel("Road Surface Conditions")
plt.title("Impact of Road Surface Conditions on Accidents")
plt.tight_layout()
plt.show()

# Create an accident heatmap based on latitude and longitude
map_center = [dataset["Latitude"].mean(), dataset["Longitude"].mean()]
accident_map = folium.Map(location=map_center, zoom_start=10)
heat_data = list(zip(dataset["Latitude"], dataset["Longitude"]))
HeatMap(heat_data).add_to(accident_map)

# Save map as HTML
accident_map.save("accident_hotspots.html")

print("Analysis completed. Heatmap saved as 'accident_hotspots.html'.")
