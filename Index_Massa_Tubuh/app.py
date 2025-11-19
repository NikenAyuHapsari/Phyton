import streamlit as st

def hitung_imt(berat_kg, tinggi_m):
    """Menghitung Indeks Massa Tubuh (IMT) = berat / tinggi^2."""
    if tinggi_m > 0:
        imt = berat_kg / (tinggi_m ** 2)
        return imt
    return 0 

def tentukan_kategori(imt):
    """Menentukan kategori IMT."""
    if imt < 18.5:
        return "Kurus/Kekurangan berat badan", "warning"
    elif 18.5 <= imt < 25.0:
        return "Normal/Ideal", "success"
    elif 25.0 <= imt < 30.0:
        return "Kelebihan berat badan", "warning"
    else:
        return "Obesitas", "error"

# --- Judul dan Deskripsi Aplikasi Streamlit ---
st.title("⚖️ Kalkulator Indeks Massa Tubuh (IMT)")
st.markdown("Masukkan data Anda ke dalam **kotak teks** di bawah ini untuk menghitung IMT.")

# --- Input Menggunakan Widget st.text_input ---
col1, col2 = st.columns(2)

with col1:
    # Menggunakan st.text_input untuk Berat
    berat_str = st.text_input(
        'Masukkan Berat Badan Anda (kg):', 
        value="60.0", 
        placeholder="Contoh: 60.5"
    )

with col2:
    # Menggunakan st.text_input untuk Tinggi
    tinggi_str = st.text_input(
        'Masukkan Tinggi Badan Anda (meter):', 
        value="1.70",
        placeholder="Contoh: 1.70"
    )

# Tombol untuk memicu perhitungan
if st.button("Hitung IMT"):
    try:
        # Konversi input string ke float
        berat = float(berat_str)
        tinggi = float(tinggi_str)

        if berat > 0 and tinggi > 0:
            # Panggil fungsi hitung IMT
            hasil_imt = hitung_imt(berat, tinggi)
            
            # Panggil fungsi tentukan kategori
            kategori, gaya = tentukan_kategori(hasil_imt)
            
            # --- Output Menggunakan Streamlit ---
            st.subheader("📊 Hasil Perhitungan IMT")
            st.write(f"Nilai IMT Anda adalah: **{hasil_imt:.2f}**")
            
            if gaya == "success":
                st.success(f"Kategori: {kategori}")
            elif gaya == "warning":
                st.warning(f"Kategori: {kategori}")
            else:
                st.error(f"Kategori: {kategori}")

        else:
            st.error("⚠️ Berat badan dan tinggi badan harus lebih besar dari 0.")
            
    except ValueError:
        # Menangani jika input bukan angka
        st.error("❌ **Error:** Pastikan Anda memasukkan nilai numerik (angka) yang valid.")