import streamlit as st

def hitung_luas(panjang, lebar):
    """Menghitung Luas = Panjang * Lebar"""
    luas = panjang * lebar
    return luas

# --- Judul Aplikasi Streamlit ---
st.title("📏 Kalkulator Luas Persegi Panjang")
st.markdown("Aplikasi sederhana untuk menghitung luas berdasarkan panjang dan lebar.")

# --- Input Menggunakan Widget Streamlit ---
# st.number_input digunakan untuk input angka
panjang = st.number_input("Masukkan Panjang:", min_value=0.0, step=0.1)
lebar = st.number_input("Masukkan Lebar:", min_value=0.0, step=0.1)

# Tombol untuk memicu perhitungan (opsional, bisa juga dihitung langsung)
if st.button("Hitung Luas"):
    # Cek jika input valid (tidak 0, meskipun min_value sudah 0.0)
    if panjang > 0 and lebar > 0:
        # Panggil fungsi
        hasil_luas = hitung_luas(panjang, lebar)
        
        # --- Output Menggunakan Streamlit ---
        st.success(f"✅ Luas Persegi Panjang adalah: **{hasil_luas:.2f}**")
        
        st.balloons() # Efek visual
    else:
        st.warning("⚠️ Pastikan Panjang dan Lebar lebih besar dari nol.")