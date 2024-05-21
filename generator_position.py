import folium
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = 'Malgun Gothic'

df = pd.read_csv("data_csv/발전소 현황.csv")

icon_dict = {"수력":"water", "기력":"industry", "복합화력":"fire", "원자력":"radiation", "집단":"shower", "내연력":"industry", "기타":"industry"}
color_dict = {"수력":"blue", "기력":"darkred", "복합화력":"red", "원자력":"orange", "집단":"lightred", "내연력":"black", "기타":"purple"}
company_list = ["한수원", "수자원공사", "동서발전", "남부발전", "남동발전", "중부발전", "서부발전", "기타"]

for company in company_list:
    m = folium.Map(location=(36.0, 127.0), zoom_start=8, tiles="Cartodb Positron")
    if company != "기타": new_df = df[df["소속사"] == company]
    else: new_df = df[~df["소속사"].isin(company_list[:-1])]
    for idx, row in new_df.iterrows():
        name, latitude, longtitude, icon, color = row["발전소명"], row["위도"], row["경도"], icon_dict[row["발전종류 대분류"]], color_dict[row["발전종류 대분류"]]
        folium.Marker(location=(latitude, longtitude),
                      popup=name,
                      icon=folium.Icon(
                          color=color,
                          icon_color="white",
                          icon=icon,
                          prefix="fa",
                          )).add_to(m)
    m.save(f'data_map/{company}_map.html')

sns.scatterplot(data=df, x="경도", y="위도", hue="발전종류 대분류")
plt.show()