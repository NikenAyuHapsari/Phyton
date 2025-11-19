import streamlit as st

def urutkan_bilangan(a, b, c):
    """Mengurutkan tiga bilangan dari yang terkecil ke terbesar."""
    
    # Konversi input ke list
    bilangan = [a, b, c]
    
    # Menggunakan fungsi sorted() untuk efisiensi
    # hasil_urut = sorted(bilangan)
    # return hasil_urut
    
    # Menggunakan logika if/elif yang mendekati program asli Anda:
    
    if a == max(bilangan):
        if b > c:
            hasil_urut = [c, b, a]
        else:
            hasil_urut = [b, c, a]
    elif b == max(bilangan):
        if a > c:
            hasil_urut = [c, a, b]
        else:
            hasil_urut = [a, c, b]
    else: # c == max(bilangan)
        if a > b:
            hasil_urut = [b, a, c]
        else:
            hasil_urut = [a, b, c]
            
    return hasil_urut

# --- Judul Aplikasi Streamlit ---
st.title("🔢 Pengurut Tiga Bilangan")
st.markdown("Masukkan tiga bilangan bulat untuk diurutkan dari yang terkecil hingga terbesar.")

# --- Input Menggunakan Widget Streamlit ---
# st.number_input untuk input bilangan bulat (int)
bil_a = st.number_input("Masukkan bilangan pertama (A):", value=0, step=1)
bil_b = st.number_input("Masukkan bilangan kedua (B):", value=0, step=1)
bil_c = st.number_input("Masukkan bilangan ketiga (C):", value=0, step=1)

# Tombol untuk memicu perhitungan
if st.button("Urutkan!"):
    # Panggil fungsi pengurutan
    hasil_urut = urutkan_bilangan(bil_a, bil_b, bil_c)
    
    # Format output
    output_string = ", ".join(map(str, hasil_urut))
    
    # Tampilkan hasil
    st.success(f"✅ Urutan bilangan dari yang paling kecil adalah: **{output_string}**")