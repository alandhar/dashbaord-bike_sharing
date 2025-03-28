import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day = pd.read_csv("./data/day.csv")
hour = pd.read_csv("./data/hour.csv")

# Cleaning & Preprocessing
hour['dteday'] = pd.to_datetime(hour['dteday'])
day['dteday'] = pd.to_datetime(day['dteday'])

# Map categorical values
weather_map = {
    1: "Clear / Few Clouds",
    2: "Mist / Cloudy",
    3: "Light Rain / Snow",
    4: "Heavy Rain / Snow"
}
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
workingday_map = {0: "Libur / Akhir Pekan", 1: "Hari Kerja"}

hour['season'] = hour['season'].map(season_map)
hour['weathersit'] = hour['weathersit'].map(weather_map)
hour['workingday_label'] = hour['workingday'].map(workingday_map)

# Sidebar filters
st.sidebar.title("Filter Dashboard")
user_type = st.sidebar.multiselect("Pilih Tipe Pengguna", ["Casual", "Registered"], default=["Casual", "Registered"])
selected_workingday = st.sidebar.multiselect("Pilih Jenis Hari", ["Hari Kerja", "Libur / Akhir Pekan"], default=["Hari Kerja", "Libur / Akhir Pekan"])

# Filter data sesuai pilihan
filtered_hour = hour.copy()
filtered_hour = filtered_hour[filtered_hour['workingday_label'].isin(selected_workingday)]

# Streamlit Page Setup
st.title("Bike Sharing Dashboard")

# Summary Metrics
st.subheader("Summary Metrics")
total_rentals = day['cnt'].sum()
total_casual = day['casual'].sum()
total_registered = day['registered'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", f"{total_rentals:,}")
col2.metric("Casual Users", f"{total_casual:,}")
col3.metric("Registered Users", f"{total_registered:,}")

# Section - Peminjaman Berdasarkan Jam dan Workingday
st.markdown("---")
st.subheader("Rata-rata Peminjaman per Jam Berdasarkan Jenis Hari")
fig, ax = plt.subplots(figsize=(15, 8))
grouped = filtered_hour.groupby(['hr', 'workingday_label']).agg({
    'casual': 'mean',
    'registered': 'mean',
    'cnt': 'mean'
}).reset_index()

if user_type == ["Casual"]:
    sns.lineplot(data=grouped, x='hr', y='casual', hue='workingday_label', ax=ax, marker='o')
elif user_type == ["Registered"]:
    sns.lineplot(data=grouped, x='hr', y='registered', hue='workingday_label', ax=ax, marker='o')
else:
    sns.lineplot(data=grouped, x='hr', y='cnt', hue='workingday_label', ax=ax, marker='o')

ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Jumlah Peminjaman")
ax.set_title("Rata-rata Peminjaman Sepeda per Jam")
ax.legend(title="Jenis Hari")
ax.grid(True)
plt.tight_layout() 
st.pyplot(fig)

st.markdown("---")
st.subheader("Tren Harian Peminjaman: Casual vs Registered vs Total")
day_filtered = day.copy()
fig, ax = plt.subplots(figsize=(15, 8))
if user_type == ["Casual"]:
    ax.plot(day_filtered['dteday'], day_filtered['casual'], label='Casual', color='skyblue')
elif user_type == ["Registered"]:
    ax.plot(day_filtered['dteday'], day_filtered['registered'], label='Registered', color='orange')
else:
    if set(user_type) == {"Casual", "Registered"}:
        ax.plot(day_filtered['dteday'], day_filtered['cnt'], label='Total', color='green')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Peminjaman')
ax.set_title('Tren Peminjaman Sepeda per Hari')
ax.legend()
ax.grid(True)
plt.tight_layout()
st.pyplot(fig)


# Section - Rata-rata Peminjaman Berdasarkan Cuaca
st.markdown("---")
st.subheader("Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman")
weather_avg = filtered_hour.groupby('weathersit').agg({'cnt': 'mean'}).reset_index()
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(data=weather_avg, x='weathersit', y='cnt', palette='Set2', ax=ax)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Peminjaman")
ax.set_title("Rata-rata Jumlah Peminjaman Sepeda per Kondisi Cuaca")
st.pyplot(fig)

# Section - Rata-rata Peminjaman Berdasarkan Musim
st.markdown("---")
st.subheader("Distribusi Peminjaman Berdasarkan Musim")
season_avg = filtered_hour.groupby('season').agg({'cnt': 'mean'}).reset_index()
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(data=season_avg, x='season', y='cnt', palette='pastel', ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Peminjaman")
ax.set_title("Rata-rata Jumlah Peminjaman Sepeda per Musim")
st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("Bike Sharing Dashboard | Dataset: Capital Bikeshare")