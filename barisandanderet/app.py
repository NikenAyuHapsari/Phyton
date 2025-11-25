# ... (Semua fungsi di atas dipertahankan) ...

# --- C. Struktur Aplikasi Streamlit Utama ---

st.set_page_config(layout="wide")

st.title("🔢 Virtual Lab Barisan & Deret")
# ... (Deskripsi) ...
st.divider()

# Menggunakan Tabs
tab_aritmatika, tab_geometri = st.tabs(["➕ Barisan & Deret Aritmatika", "✖️ Barisan & Deret Geometri"])

# --- TAB ARITMATIKA ---
with tab_aritmatika:
    col_input, col_output = st.columns([1, 1])

    with col_input:
        st.subheader("Parameter Barisan Aritmatika")
        
        # Input
        a_arit = st.number_input("Suku Awal (a)", value=2, step=1, key='a_arit')
        b = st.slider("Beda (b)", -5, 5, 3, key='b')
        n_arit = st.slider("Jumlah Suku (n)", 2, 20, 10, key='n_arit')
        
        # Perhitungan
        suku_arit, sn_arit = hitung_aritmatika(a_arit, b, n_arit)
        
        st.subheader("Hasil Perhitungan")
        # --- BARIS YANG DIPERBAIKI (MENGHILANGKAN {n} DARI LATEX) ---
        st.metric(label=f"Jumlah {n_arit} Suku Pertama ($S_N$)", value=f"{sn_arit:.2f}")
        st.metric(label=f"Suku Terakhir ($U_N$)", value=f"{suku_arit[-1]:.2f}")
        # --------------------------------------------------------

    with col_output:
        st.subheader("Visualisasi Pertumbuhan Barisan")
        plot_barisan(suku_arit, "Aritmatika")
        
        st.subheader("Tabel Barisan")
        df_arit = pd.DataFrame({
            "n": np.arange(1, n_arit + 1),
            "Un (Suku ke-n)": suku_arit,
            "Sn (Jumlah Parsial)": np.cumsum(suku_arit) 
        })
        st.dataframe(df_arit, hide_index=True)


# --- TAB GEOMETRI ---
with tab_geometri:
    col_input, col_output = st.columns([1, 1])
    
    with col_input:
        st.subheader("Parameter Barisan Geometri")
        
        # Input
        a_geo = st.number_input("Suku Awal (a)", value=3, step=1, key='a_geo')
        r = st.slider("Rasio (r)", -2.0, 3.0, 2.0, 0.1, key='r')
        n_geo = st.slider("Jumlah Suku (n)", 2, 15, 8, key='n_geo')
        
        if abs(r) >= 1.0:
            st.warning("Peringatan: Jika |r| ≥ 1, deret tak hingga adalah divergen.")
        
        # Perhitungan
        suku_geo, sn_geo = hitung_geometri(a_geo, r, n_geo)
        
        st.subheader("Hasil Perhitungan")
        # --- BARIS YANG DIPERBAIKI (MENGHILANGKAN {n} DARI LATEX) ---
        st.metric(label=f"Jumlah {n_geo} Suku Pertama ($S_N$)", value=f"{sn_geo:.2f}")
        st.metric(label=f"Suku Terakhir ($U_N$)", value=f"{suku_geo[-1]:.2f}")
        # ---------------------------------------------------------

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
