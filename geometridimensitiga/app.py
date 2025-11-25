import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# --- Konfigurasi Halaman Utama ---
st.set_page_config(
    page_title="Virtual Lab Bangun Ruang 3D",
    page_icon="🧊",
    layout="wide"
)

st.title("🧊 Virtual Lab: Geometri Dimensi Tiga Lengkap")
st.markdown("Eksplorasi interaktif Volume dan Luas Permukaan berbagai bangun ruang.")

# Definisikan konstanta PI
PI = math.pi

# ----------------------------------------------------------------------
#                         SIDEBAR (INPUT - KIRI)
# ----------------------------------------------------------------------

st.sidebar.header("⚙️ Pengaturan Bangun Ruang")

# Pilihan Tipe Bangun Ruang
bangun_ruang = st.sidebar.selectbox(
    "Pilih Bangun Ruang:",
    ("Kubus", "Balok", "Prisma Segitiga", "Limas Segiempat", "Kerucut", "Tabung", "Bola")
)

st.sidebar.subheader("Input Dimensi")

# ----------------------------------------------------------------------
#                      FUNGSI PERHITUNGAN & RUMUS
# ----------------------------------------------------------------------

# Kontainer untuk menyimpan hasil
hasil = {}

if bangun_ruang == "Kubus":
    s = st.sidebar.number_input("Panjang Rusuk ($s$):", min_value=1.0, value=5.0, step=0.5)
    
    hasil['Volume'] = s ** 3
    hasil['Luas Permukaan'] = 6 * (s ** 2)
    rumus = {"Volume": "V = s^3", "Luas Permukaan": "LP = 6 \\cdot s^2"}
    
elif bangun_ruang == "Balok":
    p = st.sidebar.number_input("Panjang ($p$):", min_value=1.0, value=6.0, step=0.5)
    l = st.sidebar.number_input("Lebar ($l$):", min_value=1.0, value=4.0, step=0.5)
    t = st.sidebar.number_input("Tinggi ($t$):", min_value=1.0, value=3.0, step=0.5)
    
    hasil['Volume'] = p * l * t
    hasil['Luas Permukaan'] = 2 * (p * l + p * t + l * t)
    rumus = {"Volume": "V = p \\cdot l \\cdot t", "Luas Permukaan": "LP = 2(pl + pt + lt)"}

elif bangun_ruang == "Prisma Segitiga":
    alas_segitiga = st.sidebar.number_input("Alas Segitiga ($a$):", min_value=1.0, value=4.0, step=0.5)
    tinggi_segitiga = st.sidebar.number_input("Tinggi Segitiga ($t_s$):", min_value=1.0, value=3.0, step=0.5)
    tinggi_prisma = st.sidebar.number_input("Tinggi Prisma ($T$):", min_value=1.0, value=7.0, step=0.5)
    
    luas_alas = 0.5 * alas_segitiga * tinggi_segitiga
    
    # Asumsi Prisma tegak dengan alas segitiga siku-siku, sisi miring:
    sisi_miring = math.sqrt(alas_segitiga**2 + tinggi_segitiga**2) 
    keliling_alas = alas_segitiga + tinggi_segitiga + sisi_miring

    hasil['Volume'] = luas_alas * tinggi_prisma
    hasil['Luas Permukaan'] = 2 * luas_alas + keliling_alas * tinggi_prisma
    rumus = {"Volume": "V = Luas_{alas} \\cdot T", "Luas Permukaan": "LP = 2 \\cdot Luas_{alas} + K_{alas} \\cdot T"}

elif bangun_ruang == "Limas Segiempat":
    sisi_alas_p = st.sidebar.number_input("Panjang Alas ($p$):", min_value=1.0, value=5.0, step=0.5)
    sisi_alas_l = st.sidebar.number_input("Lebar Alas ($l$):", min_value=1.0, value=5.0, step=0.5)
    tinggi_limas = st.sidebar.number_input("Tinggi Limas ($T$):", min_value=1.0, value=6.0, step=0.5)
    
    luas_alas = sisi_alas_p * sisi_alas_l
    
    # Tinggi sisi tegak 1 (untuk sisi p)
    tinggi_sisi1 = math.sqrt(tinggi_limas**2 + (sisi_alas_l/2)**2)
    # Tinggi sisi tegak 2 (untuk sisi l)
    tinggi_sisi2 = math.sqrt(tinggi_limas**2 + (sisi_alas_p/2)**2)
    
    luas_sisi_tegak = 2 * (0.5 * sisi_alas_p * tinggi_sisi1) + 2 * (0.5 * sisi_alas_l * tinggi_sisi2)

    hasil['Volume'] = (1/3) * luas_alas * tinggi_limas
    hasil['Luas Permukaan'] = luas_alas + luas_sisi_tegak
    rumus = {"Volume": "V = \\frac{1}{3} \\cdot Luas_{alas} \\cdot T", "Luas Permukaan": "LP = Luas_{alas} + Luas_{sisi \\, tegak}"}

elif bangun_ruang == "Kerucut":
    r = st.sidebar.number_input("Jari-jari Alas ($r$):", min_value=1.0, value=3.0, step=0.5)
    t = st.sidebar.number_input("Tinggi ($t$):", min_value=1.0, value=4.0, step=0.5)
    
    s_kerucut = math.sqrt(r**2 + t**2) # Garis pelukis
    
    luas_alas = PI * (r ** 2)
    luas_selimut = PI * r * s_kerucut

    hasil['Volume'] = (1/3) * PI * (r ** 2) * t
    hasil['Luas Permukaan'] = luas_alas + luas_selimut
    rumus = {"Volume": "V = \\frac{1}{3} \\cdot \\pi \\cdot r^2 \\cdot t", "Luas Permukaan": "LP = \\pi r (r + s)"}

elif bangun_ruang == "Tabung":
    r = st.sidebar.number_input("Jari-jari Alas ($r$):", min_value=1.0, value=3.0, step=0.5)
    t = st.sidebar.number_input("Tinggi ($t$):", min_value=1.0, value=6.0, step=0.5)
    
    luas_alas = PI * (r ** 2)
    luas_selimut = 2 * PI * r * t

    hasil['Volume'] = PI * (r ** 2) * t
    hasil['Luas Permukaan'] = 2 * luas_alas + luas_selimut
    rumus = {"Volume": "V = \\pi \\cdot r^2 \\cdot t", "Luas Permukaan": "LP = 2 \\pi r (r + t)"}

elif bangun_ruang == "Bola":
    r = st.sidebar.number_input("Jari-jari ($r$):", min_value=1.0, value=4.0, step=0.5)
    
    hasil['Volume'] = (4/3) * PI * (r ** 3)
    hasil['Luas Permukaan'] = 4 * PI * (r ** 2)
    rumus = {"Volume": "V = \\frac{4}{3} \\cdot \\pi \\cdot r^3", "Luas Permukaan": "LP = 4 \\pi r^2"}


# ----------------------------------------------------------------------
#                      FUNGSI VISUALISASI 3D (Plotly)
# ----------------------------------------------------------------------

def buat_plot_3d(bentuk, dimensi):
    fig = go.Figure()
    
    if bentuk == "Kubus":
        s = dimensi['s']
        # Definisi titik kubus
        x = [0, s, s, 0, 0, s, s, 0]
        y = [0, 0, s, s, 0, 0, s, s]
        z = [0, 0, 0, 0, s, s, s, s]
        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 7]
        k = [0, 7, 2, 3, 6, 5, 1, 1, 3, 2, 5, 4]
        
        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, opacity=0.5, color='lightblue', name='Kubus'))
        
    elif bentuk == "Balok":
        p, l, t = dimensi['p'], dimensi['l'], dimensi['t']
        x = [0, p, p, 0, 0, p, p, 0]
        y = [0, 0, l, l, 0, 0, l, l]
        z = [0, 0, 0, 0, t, t, t, t]
        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 7]
        k = [0, 7, 2, 3, 6, 5, 1, 1, 3, 2, 5, 4]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, opacity=0.5, color='orange', name='Balok'))

    elif bentuk == "Tabung":
        r, t = dimensi['r'], dimensi['t']
        u, v = np.mgrid[0:2*PI:50j, 0:t:1j]
        x = r * np.cos(u)
        y = r * np.sin(u)
        z = v

        fig.add_trace(go.Surface(x=x, y=y, z=z, surfacecolor=np.full_like(x, 0), opacity=0.5, color='green', showscale=False, name='Selimut'))
        
        # Alas dan Tutup
        fig.add_trace(go.Surface(x=[r*np.cos(u[:,0])], y=[r*np.sin(u[:,0])], z=[np.zeros_like(u[:,0])], surfacecolor=np.full_like(u[:,0], 0), opacity=0.6, showscale=False, name='Alas'))
        fig.add_trace(go.Surface(x=[r*np.cos(u[:,0])], y=[r*np.sin(u[:,0])], z=[np.full_like(u[:,0], t)], surfacecolor=np.full_like(u[:,0], 0), opacity=0.6, showscale=False, name='Tutup'))

    elif bentuk == "Bola":
        r = dimensi['r']
        u, v = np.mgrid[0:2*PI:50j, 0:PI:50j]
        x = r * np.cos(u) * np.sin(v)
        y = r * np.sin(u) * np.sin(v)
        z = r * np.cos(v)
        
        fig.add_trace(go.Surface(x=x, y=y, z=z, surfacecolor=z, colorscale='Reds', opacity=0.8, name='Bola'))
        
    else:
        # Untuk Prisma, Limas, Kerucut, gunakan placeholder atau tampilkan informasi
        fig.update_layout(annotations=[dict(text="Visualisasi 3D Kompleks (Plotly) Tidak Tersedia untuk bentuk ini.", 
                                           showarrow=False, xref="paper", yref="paper", x=0.5, y=0.5)])
    
    # Pengaturan umum plot 3D
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            aspectmode='data'
        ),
        title=f"Model 3D Interaktif {bentuk}",
        height=550,
        margin=dict(l=0, r=0, b=0, t=30)
    )
    return fig

# ----------------------------------------------------------------------
#                         MAIN AREA (OUTPUT - KANAN)
# ----------------------------------------------------------------------

st.header(f"Analisis **{bangun_ruang}**")
st.markdown("---")

# Area untuk Plot dan Hasil (Layout Dua Kolom)
col_result, col_plot = st.columns([1, 2])

# Dapatkan dimensi untuk plotting
dimensi = {}
if bangun_ruang == "Kubus": dimensi = {'s': s}
elif bangun_ruang == "Balok": dimensi = {'p': p, 'l': l, 't': t}
elif bangun_ruang == "Tabung": dimensi = {'r': r, 't': t}
elif bangun_ruang == "Bola": dimensi = {'r': r}
else: dimensi = None


with col_plot:
    st.subheader("Visualisasi Interaktif (Plotly)")
    if dimensi:
        fig = buat_plot_3d(bangun_ruang, dimensi)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Placeholder untuk bentuk yang lebih kompleks
        st.warning(f"Visualisasi 3D interaktif untuk **{bangun_ruang}** tidak didukung dalam skrip ini.")
        st.markdown(f"**{bangun_ruang}** adalah bangun ruang yang sering digunakan. ")


with col_result:
    st.subheader("📝 Hasil Perhitungan")
    
    # Tampilkan Dimensi
    if bangun_ruang == "Kubus": st.markdown(f"* $s$ = {s}")
    elif bangun_ruang == "Balok": st.markdown(f"* $p$ = {p}, $l$ = {l}, $t$ = {t}")
    elif bangun_ruang == "Prisma Segitiga": st.markdown(f"* Alas Segitiga ($a$) = {alas_segitiga}, Tinggi Segitiga ($t_s$) = {tinggi_segitiga}, Tinggi Prisma ($T$) = {tinggi_prisma}")
    elif bangun_ruang == "Limas Segiempat": st.markdown(f"* Panjang Alas ($p$) = {sisi_alas_p}, Lebar Alas ($l$) = {sisi_alas_l}, Tinggi Limas ($T$) = {tinggi_limas}")
    elif bangun_ruang == "Kerucut" or bangun_ruang == "Tabung": st.markdown(f"* $r$ = {r}, $t$ = {t}")
    elif bangun_ruang == "Bola": st.markdown(f"* $r$ = {r}")
        
    st.markdown("---")

    # Tampilkan Rumus Volume
    st.markdown("**Volume ($V$)**")
    st.latex(rumus["Volume"])
    st.metric("Hasil Volume", f"{hasil['Volume']:,.4f} satuan kubik")

    # Tampilkan Rumus Luas Permukaan
    st.markdown("**Luas Permukaan ($LP$)**")
    st.latex(rumus["Luas Permukaan"])
    st.metric("Hasil Luas Permukaan", f"{hasil['Luas Permukaan']:,.4f} satuan persegi")

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info("Aplikasi menggunakan Plotly untuk model 3D interaktif.")
