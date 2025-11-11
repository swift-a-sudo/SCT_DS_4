import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from IPython.display import display
from google.colab import files

sns.set(style="whitegrid")
plt.rcParams["figure.dpi"]=120

print("Please upload your 'US_Accidents_Sample.csv' file:")
uploaded=files.upload()
filename=list(uploaded.keys())[0]
df=pd.read_csv(filename)
print(f"Loaded file: {filename} — {df.shape[0]} rows, {df.shape[1]} columns")

def classify_road(row):
    weather=str(row['Weather_Condition']).lower()
    precip=row['Precipitation(in)'] if not pd.isna(row['Precipitation(in)']) else 0
    vis=row['Visibility(mi)'] if not pd.isna(row['Visibility(mi)']) else 10
    if 'snow' in weather or 'ice' in weather:
        return 'Snow/Ice'
    elif 'rain' in weather or precip>0.05:
        return 'Wet'
    elif 'fog' in weather or 'mist' in weather or vis<2:
        return 'Foggy'
    elif 'storm' in weather or 'thunder' in weather:
        return 'Stormy'
    else:
        return 'Clear'

df['Road_Condition']=df.apply(classify_road,axis=1)
print("Derived Road_Condition from weather and precipitation")

plt.figure(figsize=(9,4))
top_weather=df['Weather_Condition'].value_counts().nlargest(8).index
sns.countplot(y='Weather_Condition',data=df[df['Weather_Condition'].isin(top_weather)],
              order=top_weather,palette='mako')
plt.title("Top 8 Weather Conditions During Accidents")
plt.tight_layout()
plt.show()

plt.figure(figsize=(7,4))
sns.countplot(y='Road_Condition',data=df,
              order=df['Road_Condition'].value_counts().index,
              palette='coolwarm')
plt.title("Accidents by Derived Road Condition")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,4))
sns.boxplot(x='Road_Condition',y='Severity',data=df,
            order=['Clear','Wet','Snow/Ice','Foggy','Stormy'])
plt.title("Accident Severity vs Road Condition")
plt.tight_layout()
plt.show()

df['Start_Time']=pd.to_datetime(df['Start_Time'])
df['Hour']=df['Start_Time'].dt.hour
df['DayOfWeek']=df['Start_Time'].dt.day_name()

plt.figure(figsize=(8,4))
sns.countplot(x='Hour',data=df,color='tomato')
plt.title("Accidents by Hour of Day")
plt.xlabel("Hour (0–23)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(5,4))
sns.countplot(x='Sunrise_Sunset',data=df,palette='viridis')
plt.title("Accidents: Daylight vs Nighttime")
plt.tight_layout()
plt.show()

center=[df['Start_Lat'].mean(),df['Start_Lng'].mean()]
m=folium.Map(location=center,zoom_start=5,tiles='CartoDB positron')
HeatMap(data=df[['Start_Lat','Start_Lng']],radius=6,blur=10).add_to(m)
m.save("us_accidents_hotspots.html")
print(f"Hotspot map created using all {len(df)} points and saved as 'us_accidents_hotspots.html'")
display(m)

print("\nAnalysis complete:")
print("• Derived road conditions (Clear / Wet / Snow-Ice / Foggy / Stormy)")
print("• Weather, lighting, and time patterns visualized")
print("• Hotspot map created with all data points")
print("• Interactive map saved as 'us_accidents_hotspots.html'")
