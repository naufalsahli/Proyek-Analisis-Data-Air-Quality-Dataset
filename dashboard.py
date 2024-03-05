import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import datetime

sns.set(style='white')

all_data = pd.read_csv("https://raw.githubusercontent.com/naufalsahli/Proyek-Analisis-Data-Air-Quality-Dataset/main/all_data%20(1).csv")
all_data.tail()

all_data.sort_values(by="datetime", inplace=True)
all_data.reset_index(inplace=True)
all_data.head(15)

def create_df_total_polutan(data) :
    df_total_polutan = data.groupby(['year','station']).sum()
    df_total_polutan.reset_index(inplace=True)
    df_total_polutan = pd.melt(df_total_polutan, id_vars=['year', 'station'], value_vars=['PM2.5', 'PM10'],
                        var_name='pollutant', value_name='sum_value')
    return df_total_polutan

df_total_polutan = create_df_total_polutan(all_data)

month_tren_df = all_data[(all_data["datetime"] >= "2017-02-01 02:00:00") & 
                (all_data["datetime"] <= "2017-02-28 02:00:00")]
week_tren_df = all_data[(all_data["datetime"] >= "2017-02-21 02:00:00") & 
                (all_data["datetime"] <= "2017-02-28 02:00:00")]

with st.sidebar:
    # Menambahkan logo
    st.image("https://raw.githubusercontent.com/naufalsahli/Proyek-Analisis-Data-Air-Quality-Dataset/main/Polusi1.jpg")

    # Feedback
    text = st.text_area("Bagaimana perasaanmu ketika udara di sekitarmu dipenuhi oleh polusi? ")
    st.write(text)

st.title('Pantauan Polusi Udara')

# Tren PM2.5
st.subheader('Tren Polutan PM2.5 Bulan Februari 2017')
col1, col2 = st.columns(2)

with col1:
    total_pol = month_tren_df['PM2.5'].sum()
    st.metric("Total Polutan", value=round(total_pol, 2))

with col2:
    mean_pol = month_tren_df['PM2.5'].mean()
    st.metric("Rata-Rata Polutan", value=round(mean_pol, 2))

fig, ax = plt.subplots(figsize=(12, 5))

# Plot setiap stasiun
colors = ['red','blue', 'green']
for i, loc in zip((1, 2, 3), ["Aotizhongxin", "Dingling", "Changping"]):
    filtered_df = month_tren_df[month_tren_df['station'] == loc]
    ax.plot(filtered_df['datetime'], filtered_df['PM2.5'], label=loc, color=colors[i % len(colors)])

# Menambahkan judul dan label sumbu
ax.set_title('Tren Konsentrasi PM2.5 Bulan Februari 2017')
ax.set_xlabel('Tanggal', size=13)
ax.set_ylabel('Konsentrasi PM10 (ug/m^3)', size=13)
ax.legend()

# Menampilkan grafik di Streamlit
st.pyplot(fig)

# Tren PM10
st.subheader('Tren Polutan PM10 Bulan Februari 2017')
col1, col2 = st.columns(2)

with col1:
    total_pol = month_tren_df['PM10'].sum()
    st.metric("Total Polutan", value=round(total_pol, 2))

with col2:
    mean_pol = month_tren_df['PM10'].mean()
    st.metric("Rata-Rata Polutan", value=round(mean_pol, 2))

fig, ax = plt.subplots(figsize=(12, 5))

# Plot setiap stasiun
colors = ['red','blue', 'green']
for i, loc in zip((1, 2, 3), ["Aotizhongxin", "Dingling", "Changping"]):
    filtered_df = month_tren_df[month_tren_df['station'] == loc]
    ax.plot(filtered_df['datetime'], filtered_df['PM10'], label=loc, color=colors[i % len(colors)])

# Menambahkan judul dan label sumbu
ax.set_title('Tren Konsentrasi PM10 Bulan Februari 2017')
ax.set_xlabel('Tanggal', size=13)
ax.set_ylabel('Konsentrasi PM10 (ug/m^3)', size=13)
ax.legend()

# Menampilkan grafik di Streamlit
st.pyplot(fig)

# Pantauan Polusi Udara Tahunan
st.subheader('Pantauan Polusi Udara Tahunan')

fig, ax = plt.subplots(figsize=(12, 5))

# Plot setiap stasiun
for loc in ["Aotizhongxin", "Dingling", "Changping"]:
    filtered_df = df_total_polutan[df_total_polutan['station'] == loc]
    sns.barplot(data=filtered_df, x="year", y="sum_value", hue="pollutant", ax=ax, errwidth=0)

    # Menambahkan judul dan label sumbu
    ax.set_title(f'Total Polutan per tahun di {loc}')
    ax.set_xlabel('Tanggal', size=13)
    ax.set_ylabel('Total Konsentrasi PM10 (ug/m^3)', size=13)
    ax.legend()

    # Menampilkan grafik di Streamlit
    st.pyplot(fig)

# Display information about cities with the highest concentrations in the last year
last_year_data = df_total_polutan[df_total_polutan['year'] == df_total_polutan['year'].max()]

highest_pm10_city = last_year_data[last_year_data['pollutant'] == 'PM10']['sum_value'].idxmax()
highest_pm25_city = last_year_data[last_year_data['pollutant'] == 'PM2.5']['sum_value'].idxmax()

highest_pm10_city_name = last_year_data.loc[highest_pm10_city, 'station']
highest_pm25_city_name = last_year_data.loc[highest_pm25_city, 'station']

st.subheader('Informasi Tahun Terakhir')
st.write(f"Pada tahun terakhir, kota dengan konsentrasi PM10 tertinggi adalah {highest_pm10_city_name}.")
st.write(f"Pada tahun terakhir, kota dengan konsentrasi PM2.5 tertinggi adalah {highest_pm25_city_name}.")
