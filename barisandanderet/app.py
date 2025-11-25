import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- A. Fungsi Perhitungan Barisan dan Deret ---

def hitung_aritmatika(a, b, n):
    """Menghitung suku ke-n (Un) dan jumlah n suku pertama (Sn) Aritmatika."""
    n_array = np.arange(1, n + 1)
    # Suku ke-n: Un = a + (n-1)b
    suku = a + (n_array - 1) * b
    # Jumlah n suku: Sn = n/2 * (2a + (n-1)b)
    jumlah_semua_suku = n / 2 * (2 * a + (n - 1) * b)
    return suku, jumlah_semua_suku

def hitung_geometri(a, r, n):
    """Menghitung suku ke-n (Un) dan jumlah n suku pertama (Sn) Geometri."""
    n_array = np.arange(1, n + 1)
    # Suku ke-n: Un = a * r^(n-1)
    suku = a * (r ** (n_array - 1))
    
    # Jumlah n suku: Sn = a * (r^n - 1) / (r - 1) (jika r != 1)
    if r == 1:
        jumlah_semua_suku = n * a
    else:
        jumlah_semua_suku = a * (r**n - 1) / (r - 1)
        
    return suku, jumlah_semua_suku

# --- B. Fungsi Plotting ---

def plot_barisan(suku, jenis):
    """Membuat plot visualisasi barisan."""
    fig, ax = plt.subplots(figsize=(10, 5))
    n_suku = len(suku)
    x_axis = np.arange(1, n_suku + 1)
    
    # Plot scatter (titik-titik suku)
    ax.scatter(x_axis, suku, color='red', zorder=5)
    
    # Plot garis penghubung
    ax.plot(x_axis, suku, color='blue', linestyle='--', alpha=0.6)
    
    ax.set_title(f"Visualisasi Barisan {jenis} ({n_suku} Suku)")
    ax.set_xlabel("Nomor Suku (n)")
    ax.set_ylabel("Nilai Suku (Un)")
    ax.set_xticks(x_axis)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    if jenis == "Geometri":
        # Gunakan skala logaritmik jika nilai suku terlalu besar untuk tampilan yang jelas
        if np.max(suku) > 1000 or np.min(suku) < -1000:
             ax.set_yscale('symlog')
             ax.set_ylabel("Nilai Suku (Un) - Skala Logaritmik")

    st.pyplot(fig)


# --- C. Struktur Aplikasi Streamlit Utama ---

st.set_page_config(layout="wide")

st.title("🔢 Virtual Lab Barisan & Deret")
st.markdown("Eksplorasi interaktif bagaimana perubahan Suku Awal $(a)$, Beda $(b)$ / Rasio $(r)$, dan Jumlah Suku $(n)$ memengaruhi Barisan dan Deret.")
st.divider()

# Menggunakan Tabs untuk memisahkan Aritmatika dan Geometri
tab_aritmatika, tab_geometri = st.tabs(["➕ Barisan & Deret Aritmatika", "✖️ Barisan & Deret Geometri"])

# --- TAB ARITMATIKA ---
with tab_aritmatika:
    col_input, col_output = st.columns([1, 1])

    with col_input:
        st.subheader("Parameter Barisan Aritmatika")
        
        # Input Suku Awal (a)
        a_arit = st.number_input("Suku Awal (a)", value=2, step=1, key='a_arit')
        
        # Input Beda (b)
        b = st.slider("Beda (b)", -5, 5, 3, key='b')
        
        # Input Jumlah Suku (n)
        n_arit = st.slider("Jumlah Suku (n)", 2, 20, 10, key='n_arit')
        
        # Perhitungan
        suku_arit, sn_arit = hitung_aritmatika(a_arit, b, n_arit)
        
        st.subheader("Hasil Perhitungan")
        st.metric(label=f"Jumlah {n_arit} Suku Pertama ($S_{n}$)", value=f"{sn_arit:.2f}")
        st.metric(label=f"Suku Terakhir ($U_{n}$)", value=f"{suku_arit[-1]:.2f}")

    with col_output:
        st.subheader("Visualisasi Pertumbuhan Barisan")
        plot_barisan(suku_arit, "Aritmatika")
        
        st.subheader("Tabel Barisan")
        df_arit = pd.DataFrame({
            "n": np.arange(1, n_arit + 1),
            "Un (Suku ke-n)": suku_arit,
            # Jumlah Suku Parsial
            "Sn (Jumlah Parsial)": np.cumsum(suku_arit) 
        })
        st.dataframe(df_arit, hide_index=True)


# --- TAB GEOMETRI ---
with tab_geometri:
    col_input, col_output = st.columns([1, 1])
    
    with col_input:
        st.subheader("Parameter Barisan Geometri")
        
        # Input Suku Awal (a)
        a_geo = st.number_input("Suku Awal (a)", value=3, step=1, key='a_geo')
        
        # Input Rasio (r)
        r = st.slider("Rasio (r)", -2.0, 3.0, 2.0, 0.1, key='r')
        
        # Input Jumlah Suku (n)
        n_geo = st.slider("Jumlah Suku (n)", 2, 15, 8, key='n_geo')
        
        # Validasi Rasio untuk Konvergensi (Deret Tak Hingga)
        if abs(r) >= 1.0:
            st.warning("Peringatan: Jika |r| ≥ 1, deret tak hingga adalah divergen.")
        
        # Perhitungan
        suku_geo, sn_geo = hitung_geometri(a_geo, r, n_geo)
        
        st.subheader("Hasil Perhitungan")
        st.metric(label=f"Jumlah {n_geo} Suku Pertama ($S_{n}$)", value=f"{sn_geo:.2f}")
        st.metric(label=f"Suku Terakhir ($U_{n}$)", value=f"{suku_geo[-1]:.2f}")

    with col_output:
        st.subheader("Visualisasi Pertumbuhan Barisan")
        plot_barisan(suku_geo, "Geometri")
        
        st.subheader("Tabel Barisan")
        df_geo = pd.DataFrame({
            "n": np.arange(1, n_geo + 1),
            "Un (Suku ke-n)": suku_geo.round(2),
            "Sn (Jumlah Parsial)": np.cumsum(suku_geo).round(2)
        })
        st.dataframe(df_geo, hide_index=True)

st.divider()
st.caption("Aplikasi ini dibuat interaktif untuk memvisualisasikan perbedaan pertumbuhan linear (Aritmatika) dan eksponensial (Geometri).")
