import streamlit as st
from scipy.optimize import linprog

st.set_page_config(page_title="Optimasi Produksi Dimsum", layout="centered")

st.title("🥟 Aplikasi Optimasi Produksi Dimsum")

st.write("Masukkan data keuntungan dan batasan sumber daya:")

# Input
profit_ayam = st.number_input("Keuntungan Dimsum Ayam (Rp)", value=5000)
profit_udang = st.number_input("Keuntungan Dimsum Udang (Rp)", value=7000)

max_ayam = st.number_input("Stok Ayam (gram)", value=4000)
max_udang = st.number_input("Stok Udang (gram)", value=3200)
max_tepung = st.number_input("Stok Tepung (gram)", value=5000)
max_waktu = st.number_input("Total Waktu Produksi (menit)", value=600)

# LP setup
c = [-profit_ayam, -profit_udang]
A = [
    [100, 0],     # ayam
    [0, 80],      # udang
    [50, 60],     # tepung
    [6, 8]        # waktu
]
b = [max_ayam, max_udang, max_tepung, max_waktu]
bounds = [(0, None), (0, None)]

# Solve LP
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

if res.success:
    x, y = res.x
    total_profit = profit_ayam * x + profit_udang * y

    st.success("✅ Solusi Optimal Ditemukan!")
    st.write(f"Dimsum Ayam (x): **{x:.0f} unit**")
    st.write(f"Dimsum Udang (y): **{y:.0f} unit**")
    st.write(f"Total Keuntungan Maksimum: **Rp {total_profit:,.0f}**")
else:
    st.error("❌ Tidak ada solusi optimal ditemukan. Periksa input Anda.")
