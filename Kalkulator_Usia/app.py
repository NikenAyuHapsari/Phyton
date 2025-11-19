import streamlit as st
from datetime import datetime

# Ambil tahun saat ini secara dinamis sebagai default, tetapi gunakan 2025 sesuai permintaan
# TAHUN_SEKARANG = datetime.now().year
TAHUN_SEKARANG = 2025 

def hitung_usia(tahun_lahir, tahun_sekarang=TAHUN_SEKARANG):
    """Menghitung usia (hanya tahun) berdasarkan tahun lahir."""
    if tahun_lahir > tahun_sekarang:
        return -1 # Nilai khusus untuk tahun lahir yang tidak valid
        
    usia = tahun_sekarang - tahun_lahir
    return usia

# --- Judul dan Deskripsi Aplikasi Streamlit ---
st.title("🎂 Kalkulator Usia (Tahun 2025)")
st.markdown(f"Aplikasi ini menghitung usia Anda di tahun **{TAHUN_SEKARANG}**.")

# --- Input Menggunakan Widget st.text_input ---
thn_lahir_str = st.text_input(
    'Masukkan Tahun Lahir Anda (misalnya: 1995):', 
    value="1995", 
    max_chars=4,
    placeholder="Contoh: 1995"
)

# Tombol untuk memicu perhitungan
if st.button("Hitung Usia"):
    try:
        # Konversi input string ke integer
        thn_lahir = int(thn_lahir_str)

        # Validasi dasar tahun lahir
        if thn_lahir < 1900 or thn_lahir > TAHUN_SEKARANG:
            st.error(f"❌ **Error:** Tahun lahir harus antara 1900 dan {TAHUN_SEKARANG}.")
        else:
            # Panggil fungsi hitung usia
            usia_saat_ini = hitung_usia(thn_lahir)
            
            # --- Output Menggunakan Streamlit ---
            st.success(
                f"🎉 Jika Anda lahir tahun **{thn_lahir}**, "
                f"usia Anda di tahun {TAHUN_SEKARANG} adalah: **{usia_saat_ini} tahun**"
            )
            
    except ValueError:
        # Menangani jika input bukan angka bulat
        st.error("❌ **Error:** Pastikan Anda memasukkan Tahun Lahir berupa angka bulat yang valid (contoh: 1995).")