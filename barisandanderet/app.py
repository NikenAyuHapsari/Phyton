import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman Utama ---
st.set_page_config(
    page_title="Virtual Lab Barisan & Deret",
    page_icon="➗",
    layout="wide"  # Menggunakan layout lebar untuk visualisasi
)

st.title("➗ Virtual Lab: Barisan dan Deret")
st.markdown("Eksplorasi interaktif Barisan Aritmatika dan Geometri.")

# ----------------------------------------------------------------------
#                         SIDEBAR (INPUT - KIRI)
# ----------------------------------------------------------------------

st.sidebar.header("⚙️ Pengaturan Barisan")

# Pilihan Tipe Barisan
tipe_barisan = st.sidebar.radio(
    "Pilih Tipe Barisan:",
    ("Aritmatika", "Geometri")
)

# Input Parameter Umum
suku_pertama = st.sidebar.number_input(
    "Suku Pertama ($a$):",
    min_value=-100.0,
    max_value=100.0,
    value=2.0,
    step=1.0
)

banyak_suku = st.sidebar.slider(
    "Banyak Suku ($n$) yang Ditampilkan:",
    min_value=2,
    max_value=20,
    value=10,
    step=1
)

# Input Parameter Spesifik
if tipe_barisan == "Aritmatika":
    st.sidebar.subheader("Barisan Aritmatika")
    beda = st.sidebar.number_input(
        "Beda ($b$):",
        min_value=-20.0,
        max_value=20.0,
        value=3.0,
        step=1.0
    )
    # Fungsi Barisan Aritmatika
    def hitung_aritmatika(a, b, n):
        suku_ke_n = a + (n - 1) * b
        jumlah_n = n / 2 * (2 * a + (n - 1) * b)
        return suku_ke_n, jumlah_n

elif tipe_barisan == "Geometri":
    st.sidebar.subheader("Barisan Geometri")
    rasio = st.sidebar.number_input(
        "Rasio ($r$):",
        min_value=-5.0,
        max_value=5.0,
        value=2.0,
        step=0.5
    )
    # Fungsi Barisan Geometri
    def hitung_geometri(a, r, n):
        suku_ke_n = a * (r ** (n - 1))
        if r != 1:
            jumlah_n = a * ((r ** n) - 1) / (r - 1)
        else:
            jumlah_n = a * n
        return suku_ke_n, jumlah_n


# ----------------------------------------------------------------------
#                         MAIN AREA (OUTPUT - KANAN)
# ----------------------------------------------------------------------

tab1, tab2 = st.tabs(["📝 Hasil Perhitungan", "📈 Visualisasi Data"])

with tab1:
    st.header(f"Hasil Eksplorasi Barisan {tipe_barisan}")
    st.markdown(f"**Parameter:** $a$ = {suku_pertama}, $n$ = {banyak_suku}")

    if tipe_barisan == "Aritmatika":
        st.markdown(f"**Beda ($b$)** = {beda}")

        # Perhitungan
        data_suku = [suku_pertama + (i - 1) * beda for i in range(1, banyak_suku + 1)]
        suku_ke_n_val, jumlah_n_val = hitung_aritmatika(suku_pertama, beda, banyak_suku)
        
        # Rumus
        st.subheader("Rumus Barisan Aritmatika")
        st.latex("U_n = a + (n-1)b")
        st.latex("S_n = \\frac{n}{2} (2a + (n-1)b)")
        
        # Hasil Akhir
        st.metric(f"Suku ke-{banyak_suku} ($U_{banyak_suku}$)", f"{suku_ke_n_val:,.2f}")
        st.metric(f"Jumlah {banyak_suku} Suku Pertama ($S_{banyak_suku}$)", f"{jumlah_n_val:,.2f}")

    elif tipe_barisan == "Geometri":
        st.markdown(f"**Rasio ($r$)** = {rasio}")

        # Perhitungan
        data_suku = [suku_pertama * (rasio ** (i - 1)) for i in range(1, banyak_suku + 1)]
        suku_ke_n_val, jumlah_n_val = hitung_geometri(suku_pertama, rasio, banyak_suku)

        # Rumus
        st.subheader("Rumus Barisan Geometri")
        st.latex("U_n = a \\cdot r^{n-1}")
        
        if rasio != 1:
            st.latex("S_n = \\frac{a(r^n - 1)}{r - 1}, \\quad r \\ne 1")
        else:
            st.latex("S_n = n \\cdot a, \\quad r = 1")
            
        # Hasil Akhir
        st.metric(f"Suku ke-{banyak_suku} ($U_{banyak_suku}$)", f"{suku_ke_n_val:,.2f}")
        st.metric(f"Jumlah {banyak_suku} Suku Pertama ($S_{banyak_suku}$)", f"{jumlah_n_val:,.2f}")


    # Tampilan Data Suku dalam Tabel
    st.subheader("Tabel Data Suku")
    df = pd.DataFrame({
        'Suku Ke- ($n$)': range(1, banyak_suku + 1),
        'Nilai Suku ($U_n$)': data_suku,
    })
    st.dataframe(df, use_container_width=True, hide_index=True)


with tab2:
    st.header("Visualisasi Perkembangan Suku")
    
    # Membuat DataFrame untuk Plot
    plot_df = pd.DataFrame({
        'n': range(1, banyak_suku + 1),
        'Un': data_suku,
        'Sn': np.cumsum(data_suku) # Menghitung Deret Kumulatif (Sn)
    })
    
    col_plot1, col_plot2 = st.columns(2)
    
    with col_plot1:
        st.subheader("Grafik Barisan (Nilai $U_n$)")
        fig_un, ax_un = plt.subplots()
        ax_un.plot(plot_df['n'], plot_df['Un'], marker='o', linestyle='-', color='teal')
        ax_un.set_xlabel("Suku Ke- ($n$)")
        ax_un.set_ylabel("Nilai Suku ($U_n$)")
        ax_un.set_title(f"Barisan {tipe_barisan}")
        ax_un.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig_un)
        # 

    with col_plot2:
        st.subheader("Grafik Deret (Jumlah $S_n$)")
        fig_sn, ax_sn = plt.subplots()
        ax_sn.bar(plot_df['n'], plot_df['Sn'], color='maroon')
        ax_sn.set_xlabel("Suku Ke- ($n$)")
        ax_sn.set_ylabel("Jumlah Suku ($S_n$)")
        ax_sn.set_title(f"Deret {tipe_barisan}")
        ax_sn.grid(axis='y', linestyle='--', alpha=0.6)
        st.pyplot(fig_sn)
        # 

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info("Aplikasi dibuat untuk tujuan edukasi interaktif.")
