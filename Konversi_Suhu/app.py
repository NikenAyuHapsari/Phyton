import streamlit as st

def konversi_celsius(celsius):
    """Fungsi untuk mengkonversi suhu dari Celsius ke skala lain."""

    # Konversi ke Fahrenheit: F = (C * 9/5) + 32
    fahrenheit = (celsius * 9/5) + 32

    # Konversi ke Reamur: R = C * 4/5
    reamur = celsius * 4/5

    # Konversi ke Kelvin: K = celsius + 273.15
    kelvin = celsius + 273.15

    return fahrenheit, reamur, kelvin

# --- Judul dan Deskripsi Aplikasi Streamlit ---
st.title("♨️ Kalkulator Konversi Suhu")
st.markdown("Masukkan nilai suhu dalam Celsius untuk mengkonversi ke Fahrenheit, Reamur, dan Kelvin.")


# --- Input Menggunakan Widget st.text_input ---
celsius_str = st.text_input(
    'Masukkan Nilai Suhu dalam Celsius (°C):', 
    value="25.0", 
    placeholder="Contoh: 25.5 atau 0"
)

# Tombol untuk memicu perhitungan
if st.button("Konversi Suhu"):
    try:
        # Konversi input string ke float
        nilai_celsius = float(celsius_str)

        # Panggil fungsi konversi
        F, R, K = konversi_celsius(nilai_celsius)

        # --- Output Menggunakan Streamlit ---
        st.subheader("✅ Hasil Konversi Suhu")
        
        # Output Suhu Awal
        st.write(f"Suhu Awal (Celsius): **{nilai_celsius:.2f} °C**")
        st.divider()

        # Output Hasil Konversi
        st.metric(label="Fahrenheit (°F)", value=f"{F:.2f}")
        st.metric(label="Reamur (°R)", value=f"{R:.2f}")
        st.metric(label="Kelvin (K)", value=f"{K:.2f}")
            
    except ValueError:
        # Menangani jika input bukan angka
        st.error("❌ **Error:** Pastikan Anda memasukkan nilai numerik (angka) yang valid untuk suhu.")