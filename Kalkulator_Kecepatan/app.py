import streamlit as st

def hitung_kecepatan(jarak_km, waktu_jam):
    """Menghitung kecepatan rata-rata (km/jam)."""

    kecepatan = jarak_km / waktu_jam
    return kecepatan

# --- Judul dan Deskripsi Aplikasi Streamlit ---
st.title("🚀 Kalkulator Kecepatan Rata-Rata")
st.markdown("Hitung kecepatan rata-rata dengan memasukkan jarak tempuh (km) dan waktu tempuh (jam).")

# --- Input Menggunakan Widget st.text_input ---

col1, col2 = st.columns(2)

with col1:
    # Input Jarak
    jarak_str = st.text_input(
        'Masukkan Jarak yang Ditempuh (km):', 
        value="100", 
        placeholder="Contoh: 100.5"
    )

with col2:
    # Input Waktu
    waktu_str = st.text_input(
        'Masukkan Waktu Tempuh (jam):', 
        value="2",
        placeholder="Contoh: 2.5"
    )

# Tombol untuk memicu perhitungan
if st.button("Hitung Kecepatan"):
    try:
        # Konversi input string ke float
        jarak = float(jarak_str)
        waktu = float(waktu_str)

        # Validasi
        if waktu <= 0:
            st.error("❌ **Error:** Waktu tempuh harus lebih besar dari nol untuk menghindari pembagian dengan nol.")
        elif jarak < 0:
             st.error("❌ **Error:** Jarak tidak boleh negatif.")
        else:
            # Panggil fungsi
            hasil_kecepatan = hitung_kecepatan(jarak, waktu)
            
            # --- Output Menggunakan Streamlit ---
            st.success(
                f"✅ Kecepatan rata-rata Anda adalah: **{hasil_kecepatan:.2f} km/jam**"
            )
            
            st.caption(f"Perhitungan: {jarak} km / {waktu} jam")

    except ValueError:
        # Menangani jika input bukan angka
        st.error("❌ **Error:** Pastikan Anda memasukkan nilai numerik (angka) yang valid untuk jarak dan waktu.")