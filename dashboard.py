import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_by_weather_sit_df(df):
    byweather_sit_df = day_df.groupby(by="weather_sit").instant.nunique().reset_index(name='count')
    weather_situation = {1: 'Sunny', 2: 'Clear', 3: 'Cloudy', 4: 'Rain'}
    byweather_sit_df['weather_situation'] = byweather_sit_df['weather_sit'].map(weather_situation)
    return byweather_sit_df
def create_monthly_rentals_df(df):
    df['dateday'] = pd.to_datetime(df['dateday'])
    monthly_rentals_df = df.resample(rule='M', on='dateday').agg({
        "instant": "nunique",  
        "count": "sum"           
    })
    monthly_rentals_df = monthly_rentals_df.reset_index()
    monthly_rentals_df.rename(columns={
        "instant": "day_count",  
        "count": "total_rentals"  
    }, inplace=True)
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
    monthly_rentals_df['month_name'] = monthly_rentals_df['dateday'].dt.month.apply(lambda x: month_names[x - 1])
    return monthly_rentals_df

day_df = pd.read_csv("day.csv")

day_df.sort_values(by="dateday", inplace=True)
day_df.reset_index(drop=True, inplace=True)
day_df['dateday'] = pd.to_datetime(day_df['dateday'])

with st.sidebar:
    st.image("logo.jpg")

by_weather_sit_df = create_by_weather_sit_df (day_df)
monthly_rentals_df = create_monthly_rentals_df (day_df)

st.header('Bike Sharing Collection Dashboard :sparkles:')

st.subheader('Monthly Rentals')

color_ = ["#72BCD4"]
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='month_name',
    y='total_rentals',
    data=monthly_rentals_df,
    palette=color_,
    ci=None,
    ax=ax
)
plt.title('Perbandingan Penyewaan Sepeda Setiap Bulannya')
plt.xlabel('')
plt.ylabel('Jumlah Pengguna Sepeda')
plt.tight_layout()
st.pyplot(fig)

st.subheader('Kondisi Sewa Berdasarkan Cuaca')

colors_ = ["#87CEEB", "#D3D3D3", "#ADD8E6", "#4682B4"]
fig, ax = plt.subplots(figsize=(10, 5))  
sns.barplot(
    y="count",
    x="weather_situation",
    data=by_weather_sit_df.sort_values(by="weather_sit", ascending=True),  
    palette=colors_,
    ax=ax  
)
ax.set_title("Rata-Rata Peminjaman Sepeda pada Setiap Kondisi Cuaca", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Penyewa")
ax.set_xlabel("Kondisi Cuaca")
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)  