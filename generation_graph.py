import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import seaborn as sns

plt.rc('font', family='NanumBarunGothic')

def generation_graph():
    df_list = [pd.read_csv(f"data_csv/result_EnergyGeneration/result_EnergyGeneration_{year}.csv", index_col="월") for year in range(2015, 2023)]
    using_columns = ["사업자(종합) 총계", "사업자(종합) 수력 소계", "사업자(종합) 기력 소계", "사업자(종합) 복합화력 소계",
                     "사업자(종합) 원자력 소계", "사업자(종합) 신재생 소계", "사업자(종합) 집단 소계", "사업자(종합) 내연력 소계"]
    new_name_columns = ["총계", "수력", "기력", "복합화력", "원자력", "신재생", "집단", "내연력"]

    df_list = [df[using_columns] for df in df_list]
    df_list = [df.rename(columns=dict(zip(using_columns, new_name_columns))) for df in df_list]
    new_df = pd.concat([df.loc["합계"] for df in df_list], axis=1).T
    new_df.index = range(2015, 2023)

    sns.lineplot(new_df.iloc[:,1:], markers=list(Line2D.markers.keys())[:7], markersize=7.5)
    plt.xlabel("년도")
    #for x,y,v in zip(new_df.index, new_df["총계"], new_df["총계"]):
    #    plt.text(x, y+1500000, f"{v/1000000:,.2f}", ha="center", va="top")
    plt.show()

def region_heatmap():
    df = pd.read_csv("data_csv/HOME_발전량_지역별.csv", index_col="연도").iloc[:8]
    df = df.map(lambda x: x/1000000)
    sns.heatmap(df, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={"label": "발전량(단위: TWh)"})
    plt.xlabel("광역자치단체")
    plt.show()
    
def region_heatmap_percentage():
    df = pd.read_csv("data_csv/HOME_발전량_지역별.csv", index_col="연도").iloc[:8]
    df = df.div(df.sum(axis=1), axis=0).mul(100)
    sns.heatmap(df, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={"label": "발전량(단위: TWh)"})
    plt.xlabel("광역자치단체")
    plt.show()
    
generation_graph()
region_heatmap()
region_heatmap_percentage()