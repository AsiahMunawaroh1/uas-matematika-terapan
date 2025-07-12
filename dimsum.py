import streamlit as st
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import numpy as np

# Konfigurasi halaman
st.set_page_config(page_title="Optimasi Produksi Dimsum", layout="centered")

st.title("🥟 Aplikasi Optimasi Produksi Dimsum")
st.markdown("**Gunakan Linear Programming untuk menentukan jumlah produksi optimal**")

# ------------------------- Input User -------------------------
st.subheader("📥 Input Data Produksi")
profit_ayam = st.number_input("Keuntungan Dimsum Ayam (Rp)", value=5000)
profit_udang = st.number_input("Keuntungan Dimsum Udang (Rp)", value=7000)

max_ayam = st.number_input("Stok Ayam (gram)", value=4000)
max_udang = st.number_input("Stok Udang (gram)", value=3200)
max_tepung = st.number_input("Stok Tepung (gram)", value=5000)
max_waktu = st.number_input("Total Waktu Produksi (menit)", value=600)

# ------------------------- Linear Programming -------------------------
c = [-profit_ayam, -profit_udang]  # Max Z → Min -Z
A = [
    [100, 0],     # Ayam
    [0, 80],      # Udang
    [50, 60],     # Tepung
    [6, 8]        # Waktu
]
b = [max_ayam, max_udang, max_tepung, max_waktu]
bounds = [(0, None), (0, None)]

res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

# ------------------------- Output Hasil -------------------------
st.subheader("📊 Hasil Optimasi")

if res.success:
    x, y = res.x
    total_profit = profit_ayam * x + profit_udang * y

    st.success("✅ Solusi Optimal Ditemukan!")
    st.write(f"- Jumlah Dimsum Ayam: **{x:.0f} unit**")
    st.write(f"- Jumlah Dimsum Udang: **{y:.0f} unit**")
    st.write(f"- Total Keuntungan Maksimal: **Rp {total_profit:,.0f}**")

    # ---------------------- Visualisasi Grafik ----------------------
    st.subheader("📈 Visualisasi Area Feasible")

    x_vals = np.linspace(0, 100, 400)
    fig, ax = plt.subplots()

    # Setiap batas kendala
    y_ayam = np.full_like(x_vals, max_udang / 80)         # Udang
    y_tepung = (max_tepung - 50 * x_vals) / 60
    y_waktu = (max_waktu - 6 * x_vals) / 8

    # Plot grafik
    ax.plot(x_vals, y_tepung, label="Kendala Tepung", color="orange")
    ax.plot(x_vals, y_waktu, label="Kendala Waktu", color="blue")
    ax.axhline(y=max_udang / 80, color='green', linestyle='--', label="Kendala Udang")

    ax.fill_between(x_vals,
                    0,
                    np.minimum(np.minimum(y_tepung, y_waktu), max_udang / 80),
                    where=(x_vals >= 0),
                    color='gray', alpha=0.2, label="Area Feasible")

    # Titik solusi optimal
    ax.plot(x, y, 'ro', label="Solusi Optimal")
    ax.set_xlim(0, max(x_vals))
    ax.set_ylim(0, max(y_tepung.max(), y_waktu.max()) + 5)
    ax.set_xlabel("Dimsum Ayam (x)")
    ax.set_ylabel("Dimsum Udang (y)")
    ax.set_title("Area Feasible dan Solusi Optimal")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

else:
    st.error("❌ Tidak ditemukan solusi optimal. Silakan periksa input.")
