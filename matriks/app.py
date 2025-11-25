import streamlit as st
import numpy as np
import pandas as pd

# --- Konfigurasi Halaman Utama ---
st.set_page_config(
    page_title="Virtual Lab Perhitungan Matriks",
    page_icon="🧮",
    layout="wide"
)

st.title("🧮 Virtual Lab: Kalkulator Matriks Interaktif")
st.markdown("Eksplorasi operasi dasar matriks: Penjumlahan, Perkalian, Transpose, Determinan, dan Invers.")

# ----------------------------------------------------------------------
#                         SIDEBAR (INPUT - KIRI)
# ----------------------------------------------------------------------

st.sidebar.header("⚙️ Pengaturan Matriks")

# 1. Pilihan Operasi
operasi = st.sidebar.selectbox(
    "Pilih Operasi Matriks:",
    ("Penjumlahan (A + B)", "Pengurangan (A - B)", "Perkalian (A x B)", 
     "Transpose (A^T)", "Determinan & Invers (A)")
)

# 2. Pengaturan Ukuran (Dimensi) Matriks
st.sidebar.subheader("Dimensi Matriks")

if "Transpose" in operasi or "Determinan & Invers" in operasi:
    # Untuk operasi unary (satu matriks)
    M_A = st.sidebar.number_input("Baris Matriks A:", min_value=1, max_value=4, value=2, step=1)
    N_A = st.sidebar.number_input("Kolom Matriks A:", min_value=1, max_value=4, value=2, step=1)
    M_B, N_B = M_A, N_A # Matriks B tidak relevan
else:
    # Untuk operasi binary (dua matriks)
    M_A = st.sidebar.number_input("Baris Matriks A:", min_value=1, max_value=4, value=2, step=1)
    N_A = st.sidebar.number_input("Kolom Matriks A:", min_value=1, max_value=4, value=2, step=1)
    
    # Atur dimensi B berdasarkan operasi
    if "Penjumlahan" in operasi or "Pengurangan" in operasi:
        M_B, N_B = M_A, N_A # Harus memiliki dimensi yang sama
    elif "Perkalian" in operasi:
        M_B = N_A # Syarat perkalian: kolom A = baris B
        N_B = st.sidebar.number_input("Kolom Matriks B:", min_value=1, max_value=4, value=2, step=1)


# 3. Input Nilai Matriks
st.sidebar.subheader("Input Nilai Matriks")

def input_matriks(label, M, N):
    st.sidebar.markdown(f"**Matriks {label} ({M} x {N})**")
    
    # Membuat input widget per elemen
    cols = st.sidebar.columns(N)
    elements = []
    
    for i in range(M):
        row = []
        for j in range(N):
            default_value = 1.0 if (i == j and M==N) else 0.0 # Default diagonal 1, lainnya 0
            
            # Key harus unik untuk setiap widget input
            key = f"{label}_{i}_{j}" 
            
            val = cols[j].number_input(
                f"[{i+1},{j+1}]", 
                value=default_value, 
                step=0.5, 
                key=key,
                label_visibility="collapsed"
            )
            row.append(val)
        elements.append(row)
    return np.array(elements)

# Panggil fungsi input
A = input_matriks('A', M_A, N_A)

if "Transpose" not in operasi and "Determinan & Invers" not in operasi:
    B = input_matriks('B', M_B, N_B)


# ----------------------------------------------------------------------
#                         MAIN AREA (OUTPUT - KANAN)
# ----------------------------------------------------------------------

st.header(f"Operasi Terpilih: **{operasi}**")
st.markdown("---")

# Tampilkan Matriks A dan B yang diinput
col_a, col_b = st.columns(2)

with col_a:
    st.subheader(f"Matriks A ({M_A} x {N_A})")
    st.dataframe(pd.DataFrame(A), use_container_width=True)

if "Transpose" not in operasi and "Determinan & Invers" not in operasi:
    with col_b:
        st.subheader(f"Matriks B ({M_B} x {N_B})")
        st.dataframe(pd.DataFrame(B), use_container_width=True)
else:
     with col_b:
        st.subheader("Operasi Matriks Unary")
        st.info("Operasi ini hanya memerlukan Matriks A.")


# --- Bagian Perhitungan ---
st.markdown("## 🎯 Hasil Perhitungan")

try:
    if operasi == "Penjumlahan (A + B)":
        Result = A + B
        st.latex("C = A + B")
        penjelasan = "Penjumlahan Matriks: Elemen yang bersesuaian pada Matriks A dan B dijumlahkan. Syarat: kedua matriks harus memiliki dimensi yang sama."
        
    elif operasi == "Pengurangan (A - B)":
        Result = A - B
        st.latex("C = A - B")
        penjelasan = "Pengurangan Matriks: Elemen yang bersesuaian pada Matriks B dikurangkan dari Matriks A. Syarat: kedua matriks harus memiliki dimensi yang sama."
        
    elif operasi == "Perkalian (A x B)":
        if N_A != M_B:
            raise ValueError("Syarat Perkalian: Kolom A harus sama dengan Baris B ($N_A = M_B$).")
        Result = A @ B # Operator perkalian matriks NumPy
        st.latex("C = A \\times B")
        penjelasan = f"Perkalian Matriks: Setiap elemen pada baris Matriks A dikalikan dengan elemen yang bersesuaian pada kolom Matriks B, kemudian dijumlahkan. Hasil matriks berdimensi {M_A} x {N_B}."
        
    elif operasi == "Transpose (A^T)":
        Result = A.T
        st.latex("A^T")
        penjelasan = f"Transpose Matriks: Baris pada Matriks A diubah menjadi kolom pada Matriks Hasil. Jika A berdimensi {M_A} x {N_A}, maka A^T berdimensi {N_A} x {M_A}."
        
    elif operasi == "Determinan & Invers (A)":
        
        if M_A != N_A:
            st.error("Determinan dan Invers hanya berlaku untuk Matriks Persegi ($M=N$).")
            st.stop()
            
        st.subheader("Determinan ($\det(A)$)")
        determinan = np.linalg.det(A)
        st.metric("Nilai Determinan", f"{determinan:,.4f}")
        
        st.subheader("Invers ($A^{-1}$)")
        
        if np.isclose(determinan, 0):
            st.warning("Determinan sama dengan nol. Matriks ini adalah **Matriks Singular** dan **tidak memiliki Invers**.")
            st.stop()
        
        Result = np.linalg.inv(A)
        st.latex("A^{-1} = \\frac{1}{\\det(A)} \\cdot adj(A)")
        penjelasan = "Invers Matriks: Matriks yang jika dikalikan dengan Matriks A akan menghasilkan Matriks Identitas. Invers hanya ada jika Matriks A adalah persegi dan determinannya tidak nol."

    else:
        Result = np.array([])
        penjelasan = "Pilih operasi dari sidebar."

    # Tampilkan Hasil
    st.markdown("### Matriks Hasil")
    st.dataframe(pd.DataFrame(Result).round(4), use_container_width=True)
    
    st.markdown("### Penjelasan Konsep")
    st.info(penjelasan)
    
    # Visualisasi Matriks Hasil
    if "Transpose" not in operasi and "Determinan & Invers" not in operasi:
        if Result.size > 0:
            st.subheader("Visualisasi Matriks Hasil")
            fig = px.imshow(Result, text_auto=True, color_continuous_scale='Viridis',
                            title=f"Visualisasi Nilai Matriks Hasil ({Result.shape[0]}x{Result.shape[1]})")
            st.plotly_chart(fig, use_container_width=True)
            

[Image of X]
 # Placeholder untuk visualisasi matriks (Heatmap)
            
except ValueError as e:
    st.error(f"⚠️ ERROR DIMENSI ATAU OPERASI: {e}")
    st.info("Periksa kembali dimensi Matriks A dan B. Pastikan memenuhi syarat operasi yang dipilih.")
except np.linalg.LinAlgError:
    st.error("⚠️ ERROR MATRIKS: Matriks ini mungkin Singular (Determinan = 0) atau tidak memiliki Invers.")


# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info("Aplikasi menggunakan NumPy untuk kalkulasi matriks.")
