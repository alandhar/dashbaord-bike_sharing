import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day = pd.read_csv("day.csv")
hour = pd.read_csv("hour.csv")

# Preprocessing
hour['dteday'] = pd.to_datetime(hour['dteday'])
day['dteday'] = pd.to_datetime(day['dteday'])

# Sidebar
st.sidebar.title("Filter Dashboard")
user_type = st.sidebar.selectbox("Pilih Tipe Pengguna", ["Semua", "casual", "registered"])
weather_map = {
    1: "Cerah / Sedikit Awan",
    2: "Berkabut / Mendung",
    3: "Hujan Ringan / Salju Ringan",
    4: "Hujan Lebat / Salju Lebat"
}
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
hour['season'] = hour['season'].map(season_map)
hour['weathersit'] = hour['weathersit'].map(weather_map)

# Header
st.title("Bike Sharing Dashboard")
st.markdown("### Ringkasan Statistik")

# Summary stats
total_cnt = day['cnt'].sum()
total_casual = day['casual'].sum()
total_registered = day['registered'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Peminjaman", f"{total_cnt:,}")
col2.metric("Pengguna Casual", f"{total_casual:,}")
col3.metric("Pengguna Registered", f"{total_registered:,}")

# Section 2 - Peminjaman Berdasarkan Waktu
st.markdown("---")
st.subheader("Peminjaman Berdasarkan Waktu")
fig, ax = plt.subplots(figsize=(15, 8))
hour_avg = hour.groupby('hr').agg({'casual': 'mean', 'registered': 'mean', 'cnt': 'mean'}).reset_index()

if user_type == "casual":
    sns.lineplot(data=hour_avg, x='hr', y='casual', label='Casual', ax=ax)
elif user_type == "registered":
    sns.lineplot(data=hour_avg, x='hr', y='registered', label='Registered', ax=ax)
else:
    sns.lineplot(data=hour_avg, x='hr', y='cnt', label='Total', ax=ax)

ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Jumlah Peminjaman")
ax.set_title("Rata-rata Peminjaman per Jam")
st.pyplot(fig)

# Section 3 - Cuaca
st.markdown("---")
st.subheader("Pengaruh Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(15, 8))
if user_type == "Semua":
    sns.boxplot(data=hour, x='weathersit', y='cnt', ax=ax)
else:
    sns.boxplot(data=hour, x='weathersit', y=user_type, ax=ax)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Pengaruh Cuaca terhadap Jumlah Peminjaman")
st.pyplot(fig)

# Section 4 - Musim & Bulan
st.markdown("---")
st.subheader("Distribusi Peminjaman per Musim dan Bulan")
fig, ax = plt.subplots(figsize=(15, 8))
if user_type == "Semua":
    sns.boxplot(data=hour, x='season', y='cnt', ax=ax)
else:
    sns.boxplot(data=hour, x='season', y=user_type, ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Distribusi Jumlah Peminjaman Berdasarkan Musim")
st.pyplot(fig)

# Section 5 - Perbandingan Casual vs Registered
st.markdown("---")
st.subheader("Perbandingan Pengguna Casual vs Registered")
total_users = pd.DataFrame({
    'Tipe Pengguna': ['casual', 'registered'],
    'Total Peminjaman': [total_casual, total_registered]
})
fig, ax = plt.subplots(figsize=(15, 8))
sns.barplot(data=total_users, x='Tipe Pengguna', y='Total Peminjaman', palette='pastel', ax=ax)
ax.set_title("Total Peminjaman berdasarkan Tipe Pengguna")
st.pyplot(fig)