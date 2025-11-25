import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats
import math

# --- Konfigurasi Halaman Utama ---
st.set_page_config(
    page_title="Virtual Lab Statistik Dasar",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Virtual Lab: Statistik Dasar")
st.markdown("Eksplorasi interaktif **Ukuran Pemusatan** dan **Penyebaran** Data Tunggal.")

# ----------------------------------------------------------------------
#                         SIDEBAR (INPUT - KIRI)
# ----------------------------------------------------------------------

st.sidebar.header("⚙️ Input Data")

# Input Data dari Pengguna
data_input = st.sidebar.text_area(
    "Masukkan Data (Pisahkan dengan koma atau spasi, contoh: 5, 7, 8, 9, 10, 10):",
    value="15, 17, 18, 18, 20, 22, 25, 25, 25, 28, 30"
)

# Pembersihan dan Konversi Data
try:
    # Mengganti koma dengan spasi jika ada, lalu memisahkan berdasarkan spasi, dan mengkonversi ke float
    data_list_str = data_input.replace(',', ' ').split()
    data = [float(x) for x in data_list_str]
    
    if len(data) < 2: # Setidaknya butuh 2 data untuk menghitung range/std dev
        st.sidebar.warning("Masukkan setidaknya dua angka untuk analisis statistik.")
        st.stop()
        
    data_np = np.array(data)
    data_np.sort() # Mengurutkan data untuk analisis
    
    st.sidebar.success(f"Jumlah Data ($N$): **{len(data_np)}**")
except Exception:
    st.sidebar.error("⚠️ Error Input Data. Pastikan data hanya berisi angka dan dipisahkan dengan benar.")
    st.stop()


st.sidebar.markdown("---")
st.sidebar.subheader("Pengaturan Visualisasi")

bins = st.sidebar.slider(
    "Jumlah Bin (Kotak) untuk Histogram:",
    min_value=5,
    max_value=20,
    value=10,
    step=1
)


# ----------------------------------------------------------------------
#                         FUNGSI PERHITUNGAN
# ----------------------------------------------------------------------

def hitung_statistik(data):
    N = len(data)
    
    # 1. Ukuran Pemusatan
    
    mean = np.mean(data)
    median = np.median(data)
    
    # Modus (Perbaikan Error SciPy stats.mode)
    mode_result = stats.mode(data)
    modus_values = mode_result.mode
    
    # Menangani kasus di mana ada Modus tunggal atau jamak
    if len(modus_values) > 0:
        modus = ", ".join([str(math.floor(m * 1000) / 1000) for m in modus_values]) # Pembulatan untuk tampilan
    else:
        modus = "Tidak ada Modus"
    
    # 2. Ukuran Penyebaran
    
    range_data = data.max() - data.min()
    
    # Variansi dan Simpangan Baku (Populasi)
    variance_pop = np.var(data)
    std_dev_pop = np.std(data)

    # Variansi dan Simpangan Baku (Sampel) - ddof=1
    variance_sampel = np.var(data, ddof=1)
    std_dev_sampel = np.std(data, ddof=1)
    
    return {
        "N": N,
        "Mean": mean,
        "Median": median,
        "Modus": modus,
        "Range": range_data,
        "Var_Pop": variance_pop,
        "Std_Pop": std_dev_pop,
        "Var_Sampel": variance_sampel,
        "Std_Sampel": std_dev_sampel,
        "Data_Sorted": data
    }

# Lakukan Perhitungan
hasil = hitung_statistik(data_np)


# ----------------------------------------------------------------------
#                         MAIN AREA (OUTPUT - KANAN)
# ----------------------------------------------------------------------
---
tab1, tab2, tab3 = st.tabs(["📊 Hasil Perhitungan", "📈 Visualisasi Data", "📝 Rumus"])

with tab1:
    st.header("Hasil Analisis Statistik Data Tunggal")

    st.subheader("Ukuran Pemusatan (Central Tendency)")
    col_mean, col_median, col_mode = st.columns(3)
    
    # Display Ukuran Pemusatan
    col_mean.metric("Rata-rata (Mean)", f"{hasil['Mean']:,.4f}")
    col_median.metric("Nilai Tengah (Median)", f"{hasil['Median']:,.4f}")
    col_mode.metric("Nilai Paling Sering (Modus)", f"{hasil['Modus']}")

    st.markdown("---")
    st.subheader("Ukuran Penyebaran (Dispersi)")

    col_range, col_var_pop, col_std_pop = st.columns(3)
    col_var_samp, col_std_samp = st.columns(2)

    # Display Ukuran Penyebaran
    col_range.metric("Rentang Data (Range)", f"{hasil['Range']:,.4f}")
    
    col_var_pop.metric("Variansi Populasi ($\sigma^2$)", f"{hasil['Var_Pop']:,.4f}")
    col_std_pop.metric("Simpangan Baku Populasi ($\sigma$)", f"{hasil['Std_Pop']:,.4f}")
    
    col_var_samp.metric("Variansi Sampel ($s^2$)", f"{hasil['Var_Sampel']:,.4f}")
    col_std_samp.metric("Simpangan Baku Sampel ($s$)", f"{hasil['Std_Sampel']:,.4f}")


    st.markdown("---")
    st.subheader("Data Input Terurut")
    st.dataframe(pd.DataFrame({'Data Terurut': hasil['Data_Sorted']}), use_container_width=True)

---
with tab2:
    st.header("Visualisasi Distribusi Data")

    col_hist, col_box = st.columns(2)
    
    df_plot = pd.DataFrame({'Nilai': data_np})
    
    with col_hist:
        st.subheader("Histogram (Distribusi Frekuensi)")
        
        # Plotly Histogram
        fig_hist = px.histogram(
            df_plot, 
            x="Nilai", 
            nbins=bins, 
            title="Histogram Data",
            labels={'Nilai':'Nilai Data'},
            color_discrete_sequence=['teal']
        )
        fig_hist.update_layout(bargap=0.05, height=450)
        st.plotly_chart(fig_hist, use_container_width=True)
        st.caption("Histogram menunjukkan bentuk distribusi data Anda.")
        

[Image of a histogram showing data distribution]


    with col_box:
        st.subheader("Box Plot (Diagram Kotak Garis)")
        
        # Plotly Box Plot
        fig_box = px.box(
            df_plot, 
            y="Nilai", 
            title="Box Plot Data",
            color_discrete_sequence=['maroon']
        )
        fig_box.update_layout(height=450)
        st.plotly_chart(fig_box, use_container_width=True)
        st.caption("Box Plot menampilkan Kuartil, Median, dan Rentang Data.")
        

[Image of a box plot illustrating quartiles and median]


---
with tab3:
    st.header("Rumus Statistik Dasar")
    
    st.subheader("1. Ukuran Pemusatan")
    
    st.markdown("**Mean (Rata-rata)**")
    st.latex(r"\bar{x} = \frac{\sum_{i=1}^{N} x_i}{N}")
    st.markdown("$N$ adalah jumlah data.")

    st.markdown("**Median**")
    st.markdown("Nilai tengah data setelah diurutkan. Jika $N$ genap, Median adalah rata-rata dua nilai tengah.")

    st.markdown("**Modus**")
    st.markdown("Nilai yang paling sering muncul dalam set data.")

    st.subheader("2. Ukuran Penyebaran (Populasi)")
    
    st.markdown("**Rentang (Range)**")
    st.latex(r"Range = X_{max} - X_{min}")

    st.markdown("**Variansi Populasi ($\sigma^2$)**")
    st.latex(r"\sigma^2 = \frac{\sum_{i=1}^{N} (x_i - \bar{x})^2}{N}")
    
    st.markdown("**Simpangan Baku Populasi ($\sigma$)**")
    st.latex(r"\sigma = \sqrt{\frac{\sum_{i=1}^{N} (x_i - \bar{x})^2}{N}}")
    st.info("Simpangan Baku (Standard Deviation) menunjukkan seberapa jauh rata-rata penyebaran nilai dari nilai rata-rata (Mean).")


# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info("Aplikasi dibuat menggunakan Python, Streamlit, Plotly, NumPy, dan SciPy.")
