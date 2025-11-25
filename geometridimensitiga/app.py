import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# --- Konfigurasi Halaman Utama ---
st.set_page_config(
    page_title="Virtual Lab Geometri Dimensi Tiga Komprehensif",
    page_icon="🧱",
    layout="wide"
)

st.title("🧱 Virtual Lab: Geometri Dimensi Tiga Komprehensif")
st.markdown("Eksplorasi interaktif **Volume** dan **Luas Permukaan** berbagai bangun ruang 3D.")

# ----------------------------------------------------------------------
#                         SIDEBAR (INPUT - KIRI)
# ----------------------------------------------------------------------

st.sidebar.header("⚙️ Pengaturan Bangun Ruang")

# Pilihan Tipe Bangun Ruang
tipe_bangun = st.sidebar.selectbox(
    "Pilih Bangun Ruang:",
    ("Kubus", "Balok", "Tabung", "Limas Segiempat", "Prisma Segitiga")
)

st.sidebar.markdown("---")
st.sidebar.subheader(f"Input Dimensi ({tipe_bangun})")

# Input Parameter Bangun Ruang Spesifik
params = {}
if tipe_bangun == "Kubus":
    s = st.sidebar.number_input("Panjang Rusuk ($s$):", min_value=1.0, value=5.0, step=0.5)
    params['s'] = s
elif tipe_bangun == "Balok":
    p = st.sidebar.number_input("Panjang ($p$):", min_value=1.0, value=7.0, step=0.5)
    l = st.sidebar.number_input("Lebar ($l$):", min_value=1.0, value=4.0, step=0.5)
    t = st.sidebar.number_input("Tinggi ($t$):", min_value=1.0, value=5.0, step=0.5)
    params = {'p': p, 'l': l, 't': t}
elif tipe_bangun == "Tabung":
    r = st.sidebar.number_input("Jari-jari Alas ($r$):", min_value=1.0, value=3.0, step=0.5)
    t = st.sidebar.number_input("Tinggi Tabung ($t$):", min_value=1.0, value=8.0, step=0.5)
    params = {'r': r, 't': t}
elif tipe_bangun == "Limas Segiempat":
    s_alas = st.sidebar.number_input("Sisi Alas ($s$):", min_value=1.0, value=6.0, step=0.5)
    t_limas = st.sidebar.number_input("Tinggi Limas ($t$):", min_value=1.0, value=7.0, step=0.5)
    params = {'s_alas': s_alas, 't': t_limas}
elif tipe_bangun == "Prisma Segitiga":
    a_alas = st.sidebar.number_input("Alas Segitiga ($a_{alas}$):", min_value=1.0, value=4.0, step=0.5)
    t_alas = st.sidebar.number_input("Tinggi Segitiga ($t_{alas}$):", min_value=1.0, value=3.0, step=0.5)
    t_prisma = st.sidebar.number_input("Tinggi Prisma ($t_{prisma}$):", min_value=1.0, value=10.0, step=0.5)
    # Untuk Luas Permukaan, anggap segitiga alas siku-siku (sisi miring c)
    c_miring = math.sqrt(a_alas**2 + t_alas**2)
    params = {'a': a_alas, 't_alas': t_alas, 't_prisma': t_prisma, 'c': c_miring}

# ----------------------------------------------------------------------
#                      FUNGSI PERHITUNGAN
# ----------------------------------------------------------------------

def hitung_sifat_bangun(tipe, p):
    V = 0
    LP = 0
    rumus_V = ""
    rumus_LP = ""

    if tipe == "Kubus":
        s = p['s']
        V = s ** 3
        LP = 6 * s ** 2
        rumus_V = "V = s^3"
        rumus_LP = "LP = 6 \\cdot s^2"
    
    elif tipe == "Balok":
        p, l, t = p['p'], p['l'], p['t']
        V = p * l * t
        LP = 2 * (p * l + p * t + l * t)
        rumus_V = "V = p \\cdot l \\cdot t"
        rumus_LP = "LP = 2(pl + pt + lt)"

    elif tipe == "Tabung":
        r, t = p['r'], p['t']
        V = math.pi * r ** 2 * t
        LP = 2 * math.pi * r * (r + t)
        rumus_V = "V = \\pi r^2 t"
        rumus_LP = "LP = 2 \\pi r(r + t)"

    elif tipe == "Limas Segiempat":
        s_alas, t = p['s_alas'], p['t']
        Luas_Alas = s_alas ** 2
        # Untuk Luas Permukaan, hitung Tinggi Sisi Tegak (tinggi segitiga, Ts)
        Ts = math.sqrt((s_alas / 2) ** 2 + t ** 2)
        Luas_Sisi_Tegak = 4 * (0.5 * s_alas * Ts)
        
        V = (1/3) * Luas_Alas * t
        LP = Luas_Alas + Luas_Sisi_Tegak
        rumus_V = "V = \\frac{1}{3} L_{alas} t"
        rumus_LP = "LP = L_{alas} + L_{sisi \\, tegak}"

    elif tipe == "Prisma Segitiga":
        a, t_alas, t_prisma, c = p['a'], p['t_alas'], p['t_prisma'], p['c']
        Luas_Alas = 0.5 * a * t_alas
        Keliling_Alas = a + t_alas + c # Asumsi Segitiga Siku-siku
        
        V = Luas_Alas * t_prisma
        LP = 2 * Luas_Alas + Keliling_Alas * t_prisma
        rumus_V = "V = L_{alas} t_{prisma}"
        rumus_LP = "LP = 2 L_{alas} + K_{alas} t_{prisma}"
        
    return V, LP, rumus_V, rumus_LP

# Fungsi untuk membuat visualisasi 3D (disederhanakan)
def buat_plot_3d(tipe, p):
    fig = go.Figure()
    
    if tipe == "Kubus":
        s = p['s']
        # Definisi koordinat kubus
        x = [0, s, s, 0, 0, s, s, 0]
        y = [0, 0, s, s, 0, 0, s, s]
        z = [0, 0, 0, 0, s, s, s, s]
        
        # Sisi-sisi yang membentuk permukaan kubus
        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
        
        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k,
                                color='lightblue', opacity=0.60))
        
    elif tipe == "Balok":
        p, l, t = p['p'], p['l'], p['t']
        x = [0, p, p, 0, 0, p, p, 0]
        y = [0, 0, l, l, 0, 0, l, l]
        z = [0, 0, 0, 0, t, t, t, t]
        
        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
        
        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k,
                                color='lightgreen', opacity=0.60))

    elif tipe == "Tabung":
        r, t = p['r'], p['t']
        # Membuat titik-titik tabung
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, t, 10)
        u, v = np.meshgrid(u, v)
        x = r * np.cos(u)
        y = r * np.sin(u)
        z = v
        
        fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Reds', opacity=0.6, showscale=False))
        
        # Alas dan Atas Tabung
        fig.add_trace(go.Surface(x=r * np.cos(u), y=r * np.sin(u), z=0 * np.ones_like(u), colorscale='Reds', opacity=0.6, showscale=False))
        fig.add_trace(go.Surface(x=r * np.cos(u), y=r * np.sin(u), z=t * np.ones_like(u), colorscale='Reds', opacity=0.6, showscale=False))
        
        
    elif tipe == "Limas Segiempat":
        s_alas, t = p['s_alas'], p['t']
        # Titik: Puncak (0,0,t), Alas (s/2, s/2, 0)
        h = s_alas / 2
        # Titik-titik
        x = [0, h, -h, -h, h]
        y = [0, h, h, -h, -h]
        z = [t, 0, 0, 0, 0]
        
        # Sisi-sisi
        i = [1, 2, 3, 4]  # Sisi Tegak
        j = [2, 3, 4, 1]
        k = [0, 0, 0, 0]
        
        # Alas
        fig.add_trace(go.Mesh3d(x=[h, -h, -h, h], y=[h, h, -h, -h], z=[0, 0, 0, 0], 
                                i=[0,0], j=[1,1], k=[2,3], color='lightgray', opacity=0.8, showlegend=False))
        
        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k,
                                color='yellow', opacity=0.60))
        
    elif tipe == "Prisma Segitiga":
        a, t_alas, t_prisma = p['a'], p['t_alas'], p['t_prisma']
        # Asumsi alas segitiga siku-siku (0,0,0), (a,0,0), (0,t_alas,0)
        
        # Koordinat 6 titik (depan dan belakang)
        X = [0, a, 0, 0, a, 0]
        Y = [0, 0, t_alas, 0, 0, t_alas]
        Z = [0, 0, 0, t_prisma, t_prisma, t_prisma]
        
        # Sisi-sisi: 2 Alas Segitiga (0,1,2) dan 3 Sisi Tegak
        i = [0, 3, 1, 4, 2, 5, 0, 1]
        j = [1, 4, 2, 5, 0, 3, 2, 3]
        k = [2, 5, 0, 3, 1, 4, 3, 4]

        fig.add_trace(go.Mesh3d(x=X, y=Y, z=Z, i=i, j=j, k=k,
                                color='pink', opacity=0.60))


    # Pengaturan Layout Umum
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'  # Memastikan rasio aspek realistis
        ),
        title=f"Model 3D Interaktif {tipe_bangun}",
        height=600,
        margin=dict(l=0, r=0, b=0, t=30)
    )
    return fig

# ----------------------------------------------------------------------
#                         MAIN AREA (OUTPUT - KANAN)
# ----------------------------------------------------------------------

V_res, LP_res, rV, rLP = hitung_sifat_bangun(tipe_bangun, params)

st.header(f"Analisis Bangun Ruang: {tipe_bangun}")
st.markdown("---")

col_plot, col_result = st.columns([3, 2])

with col_plot:
    # Tampilkan Model 3D
    try:
        fig_3d = buat_plot_3d(tipe_bangun, params)
        st.plotly_chart(fig_3d, use_container_width=True)
        # 
    except Exception as e:
        st.error(f"⚠️ Error saat visualisasi 3D: {e}")

with col_result:
    st.subheader("📝 Rumus & Hasil Perhitungan")
    
    # Menampilkan Dimensi
    st.markdown("**Dimensi Input:**")
    dim_str = ", ".join([f"${k} = {v}$" for k, v in params.items() if k not in ['c']])
    st.markdown(dim_str)
    st.markdown("---")

    # Volume
    st.metric(
        label="🚀 Volume ($V$)",
        value=f"{V_res:,.2f} satuan³"
    )
    st.markdown("**Rumus Volume:**")
    st.latex(rV)

    st.markdown("---")

    # Luas Permukaan
    st.metric(
        label="🛡️ Luas Permukaan ($LP$)",
        value=f"{LP_res:,.2f} satuan²"
    )
    st.markdown("**Rumus Luas Permukaan:**")
    st.latex(rLP)
    
    st.info("Catatan: Perhitungan Luas Permukaan Prisma Segitiga mengasumsikan alas segitiga siku-siku.")


# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info("Aplikasi menggunakan Plotly untuk visualisasi 3D interaktif.")
