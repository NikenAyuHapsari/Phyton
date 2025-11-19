import streamlit as st

def hitung_pangkat(bilangan):
    """Menghitung kuadrat (pangkat 2) dan kubik (pangkat 3) dari sebuah bilangan."""

    kuadrat = bilangan ** 2  # Pangkat 2
    kubik = bilangan ** 3    # Pangkat 3

    return kuadrat, kubik

# --- Judul dan Deskripsi Aplikasi Streamlit ---
st.title("📈 Kalkulator Pangkat")
st.markdown("Masukkan sebuah bilangan untuk menghitung nilai kuadrat (pangkat 2) dan kubik (pangkat 3)-nya.")

# --- Input Menggunakan Widget st.text_input ---
angka_str = st.text_input(
    'Masukkan sebuah bilangan:', 
    value="5", 
    placeholder="Contoh: 5, 2.5, atau -3"
)

# Tombol untuk memicu perhitungan
if st.button("Hitung Pangkat"):
    try:
        # Konversi input string ke float
        angka = float(angka_str)

        # Panggil fungsi
        hasil_kuadrat, hasil_kubik = hitung_pangkat(angka)

        # --- Output Menggunakan Streamlit ---
        st.subheader(f"✅ Hasil Pangkat dari {angka_str}")
        
        # Output Kuadrat
        st.info(f"Kuadrat (Pangkat 2): **{hasil_kuadrat:.2f}**")
        
        # Output Kubik
        st.info(f"Kubik (Pangkat 3): **{hasil_kubik:.2f}**")
            
    except ValueError:
        # Menangani jika input bukan angka
        st.error("❌ **Error:** Pastikan Anda memasukkan nilai numerik (angka) yang valid.")