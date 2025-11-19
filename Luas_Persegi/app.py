import streamlit as st

# --- Definisikan Fungsi Penghitung Luas ---
def luas_persegi(sisi):
    """Menghitung Luas = sisi * sisi"""
    luas = sisi * sisi
    return luas

# --- Judul dan Deskripsi Aplikasi Streamlit ---
st.title("📐 Kalkulator Luas Persegi")
st.markdown("Aplikasi sederhana untuk menghitung luas persegi.")

# --- Input Menggunakan Widget Streamlit ---
# st.number_input digunakan untuk menerima input angka
sisi = st.number_input(
    'Masukkan panjang sisi persegi:', 
    min_value=0, # Sisi tidak boleh negatif
    step=1,      # Menggunakan bilangan bulat
    value=0      # Nilai awal
)

# Tombol untuk memicu perhitungan
if st.button("Hitung Luas"):
    if sisi > 0:
        # Panggil fungsi
        hasil_luas = luas_persegi(sisi)
        
        # --- Output Menggunakan Streamlit ---
        st.success(f"✅ Luas persegi dengan sisi **{sisi}** adalah: **{hasil_luas}**")
    else:
        st.warning("⚠️ Panjang sisi harus lebih besar dari 0.")