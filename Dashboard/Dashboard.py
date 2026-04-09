import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load data
url = 'https://drive.google.com/uc?export=download&id=1SWWBVvwQukDmQYRAZJLIsAzHLD6pG3A6'
df = pd.read_csv(url)

# Data tanggal
df['date'] = pd.to_datetime(df[['year','month','day']])

st.title("Dashboard Analisis PM2.5 vs Suhu")

# =========================
# 1. KORELASI
# =========================
st.header("1. Korelasi TEMP vs PM2.5")

# Scatter plot
fig1, ax1 = plt.subplots()
ax1.scatter(df['TEMP'], df['PM2.5'])
ax1.set_xlabel('Temperatur')
ax1.set_ylabel('PM2.5')
ax1.set_title('Korelasi TEMP vs PM2.5')
st.pyplot(fig1)

# Korelasi total
overall_corr = df['TEMP'].corr(df['PM2.5'])
st.metric("Korelasi Total", round(overall_corr, 3))


# Korelasi per tahun
year_corr = df.groupby('year').apply(lambda x: x['TEMP'].corr(x['PM2.5']))
st.write("Korelasi per Tahun:")
st.dataframe(year_corr)

# Plot korelasi per tahun
fig2, ax2 = plt.subplots()
ax2.plot(year_corr.index, year_corr.values, marker='o')
ax2.set_xlabel('Tahun')
ax2.set_ylabel('Korelasi')
ax2.set_title('Korelasi per Tahun')
st.pyplot(fig2)

# Konsistensi kuat
kuat = (year_corr.abs() > 0.5).mean() * 100
st.write(f"Persentase |r| > 0.5: {kuat:.2f}%")

# =========================
# 2. JAM PM2.5 TERTINGGI
# =========================
st.header("2. Jam PM2.5 Tertinggi")

mean_hour = df.groupby('hour')['PM2.5'].mean()

# Plot
fig3, ax3 = plt.subplots()
ax3.plot(mean_hour.index, mean_hour.values, marker='o')
ax3.set_xlabel('Jam')
ax3.set_ylabel('Rata-rata PM2.5')
ax3.set_title('Rata-rata PM2.5 per Jam')
st.pyplot(fig3)

# Peak hour
peak_hour = mean_hour.idxmax()
peak_value = mean_hour.max()

st.metric("Jam Tertinggi", int(peak_hour))
st.write(f"Nilai PM2.5: {peak_value:.2f}")

def ambil_jam_puncak(group):
    idx = group['PM2.5'].idxmax()
    return group.loc[idx, 'hour']

daily_peak_hour = df.groupby('date').apply(ambil_jam_puncak)

consistency = (daily_peak_hour == peak_hour).mean() * 100
st.metric("Dengan konsistensi (%)", round(consistency, 2))