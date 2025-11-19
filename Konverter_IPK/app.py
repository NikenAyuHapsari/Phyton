import streamlit as st

def cek_nilai_mutu(nilai):
    """Menentukan nilai mutu (A, B, C, D, E) berdasarkan rentang."""
    
    # Cek nilai tidak valid (di luar rentang 0-100)
    if nilai > 100 or nilai < 0:
        return "Nilai Anda **tidak valid** (di luar rentang 0-100)"
    # Cek Nilai A (85-100)
    elif nilai >= 85:
        return "Nilai Anda **A**"
    # Cek Nilai B (70-84.99...)
    elif nilai >= 70:
        return "Nilai Anda **B**"
    # Cek Nilai C (55-69.99...)
    elif nilai >= 55:
        return "Nilai Anda **C**"
    # Cek Nilai D (40-54.99...)
    elif nilai >= 40:
        return "Nilai Anda **D**"
    # Sisanya adalah Nilai E (0-39.99...)
    else:
        return "Nilai Anda **E**"

# --- Judul Aplikasi Streamlit ---
st.title("💯 Pengecek Nilai Mutu Otomatis")
st.markdown("Masukkan nilai angka untuk melihat nilai mutu (A-E) Anda.")

# --- Input Menggunakan Widget Streamlit ---
# st.number_input untuk input desimal (float)
nilai_input = st.number_input(
    "Masukkan nilai Anda (0 - 100):", 
    min_value=0.0, 
    max_value=100.0, 
    step=0.1, 
    format="%.2f" # Memastikan input bisa desimal
)

# Tombol untuk memicu perhitungan
if st.button("Cek Nilai Mutu"):
    if nilai_input is not None:
        hasil = cek_nilai_mutu(nilai_input)
        
        # Tampilkan hasil
        if "tidak valid" in hasil:
            st.error(f"❌ **Error:** {hasil}")
        elif "A" in hasil or "B" in hasil:
            st.success(f"🎉 **Selamat!** {hasil}")
        else:
            st.info(f"👉 **Hasil:** {hasil}")