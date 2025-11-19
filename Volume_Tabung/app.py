import streamlit as st
import math

# --- Definisikan Fungsi Penghitung Volume Tabung ---
def hitung_volume_tabung(r, t):
    """Menghitung Volume = pi * r^2 * t"""
    # Menggunakan konstanta math.pi untuk akurasi yang lebih baik
    pi = math.pi
    volume = pi * r * r * t
    return volume

# --- Judul dan Deskripsi Aplikasi Streamlit ---
st.title("⚗️ Kalkulator Volume Tabung")
st.markdown("Hitung volume tabung dengan memasukkan jari-jari (r) dan tinggi (t).")

# --- Input Menggunakan Widget Streamlit ---
# st.number_input digunakan untuk menerima input desimal (float)
jari_jari = st.number_input(
    'Masukkan Jari-jari (r):', 
    min_value=0.0, 
    step=0.1,      
    format="%.2f", # Memastikan format desimal
    value=0.0      
)

tinggi = st.number_input(
    'Masukkan Tinggi (t):', 
    min_value=0.0, 
    step=0.1,      
    format="%.2f",
    value=0.0
)

# Tombol untuk memicu perhitungan
if st.button("Hitung Volume"):
    if jari_jari > 0 and tinggi > 0:
        # Panggil fungsi
        hasil_volume = hitung_volume_tabung(jari_jari, tinggi)
        
        # --- Output Menggunakan Streamlit ---
        st.success(f"✅ Volume tabung adalah: **{hasil_volume:.2f}** satuan kubik")
    else:
        st.warning("⚠️ Jari-jari dan tinggi harus lebih besar dari 0.")