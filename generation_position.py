import folium
import pandas as pd

df = pd.read_csv("발전소 현황.csv")
m = folium.Map(location=(36.0, 127.0), zoom_start=7, tiles="Cartodb Positron")

icon_dict = {"수력":"water", "기력":"industry", "복합화력":"fire", "원자력":"radiation", "집단":"shower"}

for row in df.iterrows():
    latitude, longtitude, icon = row["위도"], row["경도"], icon_dict[row["발전종류 대분류"]]
    folium.Marker(location=(latitude, longtitude),
                  popup='Seoul',
                  icon=folium.Icon(
                      color="red",
                      icon_color="white",
                      icon=icon,
                      prefix="fa",
                      )).add_to(m)
m.save('map.html')