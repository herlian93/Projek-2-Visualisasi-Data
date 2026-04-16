import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# =========================
# LOAD DATA
# =========================
url = 'https://drive.google.com/uc?export=download&id=1EX1rNNLY_x1zAMv8wSKGsWYEVlveOdm2'
df = pd.read_csv(url)
df['date'] = pd.to_datetime(df['date'])

st.title("Dashboard Kualitas Udara untuk Pengambilan Keputusan")

# =========================
# FILTER INTERAKTIF
# =========================
st.sidebar.header("Filter Data")

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [df['date'].min(), df['date'].max()]
)

df = df[
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1]))
]

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

df = df[df['year'].isin(selected_year)]

filtered_df = df[
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1]))
]

if filtered_df.empty:
    st.warning("Data tidak tersedia untuk rentang tanggal ini")

# =========================
# 1. POLUSI TERTINGGI
# =========================
st.header("Kapan Waktu dengan Polusi Tertinggi?")

mean_hour = df.groupby('hour')['PM2.5'].mean()

fig1, ax1 = plt.subplots()
ax1.plot(mean_hour.index, mean_hour.values, marker='o')
ax1.set_xlabel('Jam')
ax1.set_ylabel('PM2.5')
st.pyplot(fig1)

st.metric("Jam Polusi Tertinggi", int(mean_hour.idxmax()))

# =========================
# 2. WAKTU TERBAIK
# =========================
st.header("Kapan Waktu Terbaik untuk Aktivitas?")

st.metric("Jam Terbaik", int(mean_hour.idxmin()))

# =========================
# 3. POLA TAHUNAN
# =========================
st.header("Bagaimana Pola Polusi dari Waktu ke Waktu?")

yearly = df.groupby('year')['PM2.5'].mean()

fig3, ax3 = plt.subplots()
ax3.plot(yearly.index, yearly.values, marker='o')
st.pyplot(fig3)

# =========================
# REKOMENDASI
# =========================
st.header("Rekomendasi")

st.write("""
- Hindari aktivitas luar ruangan saat jam polusi tertinggi
- Lakukan aktivitas saat kualitas udara terbaik
- Waspadai kondisi tertentu seperti tidak hujan yang berpotensi meningkatkan polusi
""")
