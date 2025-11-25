import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# --- Konfigurasi Halaman Utama ---
st.set_page_config(
    page_title="Virtual Lab Geometri Dimensi Tiga",
    page_icon="🧊",
    layout="wide"
)

st.title("🧊 Virtual Lab: Geometri Dimensi Tiga (Kubus)")
st.markdown("Eksplorasi interaktif Jarak dan Sudut pada bangun ruang Kubus.")

# ----------------------------------------------------------------------
#                         SIDEBAR (INPUT - KIRI)
# ----------------------------------------------------------------------

st.sidebar.header("⚙️ Pengaturan Kubus")

sisi = st.sidebar.slider(
    "Panjang Rusuk Kubus ($s$):",
    min_value=3,
    max_value=10,
    value=6,
    step=1
)

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Perhitungan Jarak")

pilihan_jarak = st.sidebar.radio(
    "Pilih Perhitungan Jarak:",
    ("Jarak Titik ke Titik", "Jarak Titik ke Garis", "Jarak Titik ke Bidang")
)

# ----------------------------------------------------------------------
#                      FUNGSI PERHITUNGAN DAN VISUALISASI
# ----------------------------------------------------------------------

# Definisikan titik-titik Kubus (Koordinat Kartesius)
# A(0,0,0), B(s,0,0), C(s,s,0), D(0,s,0)
# E(0,0,s), F(s,0,s), G(s,s,s), H(0,s,s)
s = sisi
TITIK = {
    'A': (0, 0, 0), 'B': (s, 0, 0), 'C': (s, s, 0), 'D': (0, s, 0),
    'E': (0, 0, s), 'F': (s, 0, s), 'G': (s, s, s), 'H': (0, s, s)
}

# Fungsi untuk membuat visualisasi dasar Kubus
def buat_plot_kubus(sisi, highlight_points=None, highlight_line=None):
    # Titik-titik yang membentuk kubus
    x_coords = [0, sisi, sisi, 0, 0, sisi, sisi, 0]
    y_coords = [0, 0, sisi, sisi, 0, 0, sisi, sisi]
    z_coords = [0, 0, 0, 0, sisi, sisi, sisi, sisi]
    
    # Label titik
    labels = list(TITIK.keys())
    
    # Sisi-sisi yang membentuk kerangka kubus
    faces = [
        [0, 1, 2, 3], [4, 5, 6, 7], # Alas & Atas
        [0, 1, 5, 4], [1, 2, 6, 5], # Depan & Kanan
        [2, 3, 7, 6], [3, 0, 4, 7]  # Belakang & Kiri
    ]

    # Plot Kubus (Kerangka)
    fig = go.Figure(data=[
        go.Mesh3d(
            x=x_coords, y=y_coords, z=z_coords, 
            i=[r[0] for r in faces], j=[r[1] for r in faces], k=[r[2] for r in faces], 
            opacity=0.15, color='lightblue', name='Kubus'
        ),
        go.Scatter3d(
            x=x_coords, y=y_coords, z=z_coords, 
            mode='markers+text', 
            marker=dict(size=4, color='black'), 
            text=labels, 
            textfont=dict(size=12, color='black'),
            name='Titik Sudut'
        )
    ])
    
    # Tambahkan Garis rusuk
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0), # Alas
        (4, 5), (5, 6), (6, 7), (7, 4), # Atas
        (0, 4), (1, 5), (2, 6), (3, 7)  # Rusuk Tegak
    ]
    for i, j in edges:
        fig.add_trace(go.Scatter3d(
            x=[x_coords[i], x_coords[j]], 
            y=[y_coords[i], y_coords[j]], 
            z=[z_coords[i], z_coords[j]], 
            mode='lines', 
            line=dict(color='black', width=3), 
            showlegend=False
        ))
        
    # Highlight elemen perhitungan
    if highlight_points:
        x_hp, y_hp, z_hp = zip(*[TITIK[p] for p in highlight_points])
        fig.add_trace(go.Scatter3d(
            x=x_hp, y=y_hp, z=z_hp, 
            mode='markers+text', 
            marker=dict(size=6, color='red'),
            text=highlight_points,
            textfont=dict(size=14, color='red'),
            name='Titik Fokus'
        ))

    if highlight_line:
        p1, p2 = highlight_line
        fig.add_trace(go.Scatter3d(
            x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],
            mode='lines',
            line=dict(color='red', width=5),
            name='Jarak'
        ))

    # Pengaturan Layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, sisi], visible=False),
            yaxis=dict(range=[0, sisi], visible=False),
            zaxis=dict(range=[0, sisi], visible=False),
            aspectmode='cube'
        ),
        title=f"Kubus Rusuk $s={sisi}$",
        height=600,
        margin=dict(l=0, r=0, b=0, t=30)
    )
    return fig

# ----------------------------------------------------------------------
#                         MAIN AREA (OUTPUT - KANAN)
# ----------------------------------------------------------------------

col_info, col_plot = st.columns([1, 2.5])

with col_info:
    st.subheader("Rumus & Perhitungan")
    st.markdown(f"Panjang Rusuk Kubus ($s$) = **{sisi}**")
    st.dataframe(pd.DataFrame(TITIK, index=['x', 'y', 'z']).T.reset_index().rename(columns={'index':'Titik'}), 
                 use_container_width=True, hide_index=True)
    st.markdown("---")

    
if pilihan_jarak == "Jarak Titik ke Titik":
    with col_info:
        st.subheader("1. Jarak Titik ke Titik")
        titik1 = st.selectbox("Titik Awal:", list(TITIK.keys()), index=0) # A
        titik2 = st.selectbox("Titik Akhir:", list(TITIK.keys()), index=6) # G
        
        P1 = TITIK[titik1]
        P2 = TITIK[titik2]
        
        # Perhitungan Jarak Euklidian 3D
        jarak_val = np.sqrt(sum([(P2[i] - P1[i])**2 for i in range(3)]))
        
        st.latex(f"Jarak = \\sqrt{{(x_2-x_1)^2 + (y_2-y_1)^2 + (z_2-z_1)^2}}")
        st.latex(f"Jarak_{{{titik1}{titik2}}} = {jarak_val:.2f}")

        st.info(f"Jarak antara {titik1} dan {titik2} adalah **{jarak_val:.2f}** satuan.")

    with col_plot:
        # Visualisasi Jarak Titik ke Titik
        fig_tt = buat_plot_kubus(sisi, highlight_points=[titik1, titik2], highlight_line=[P1, P2])
        st.plotly_chart(fig_tt, use_container_width=True)

elif pilihan_jarak == "Jarak Titik ke Garis":
    
    # Simplifikasi perhitungan: Jarak dari Titik P ke Garis AB (Rusuk)
    titik_P_label = st.sidebar.selectbox("Titik P:", ['G', 'E', 'D', 'B'])
    garis_AB_label = st.sidebar.selectbox("Garis (Rusuk):", ['AB', 'BC', 'FG', 'EH'])
    
    # Ambil koordinat garis
    A_label, B_label = list(garis_AB_label)
    P = TITIK[titik_P_label]
    A = TITIK[A_label]
    B = TITIK[B_label]
    
    # Vektor Garis AB
    vec_AB = np.array(B) - np.array(A)
    # Vektor AP
    vec_AP = np.array(P) - np.array(A)

    # Perhitungan Jarak Titik ke Garis (menggunakan proyeksi vektor)
    # Jarak = |AP x AB| / |AB|
    cross_prod = np.cross(vec_AP, vec_AB)
    jarak_val = np.linalg.norm(cross_prod) / np.linalg.norm(vec_AB)

    with col_info:
        st.subheader("2. Jarak Titik ke Garis")
        st.markdown(f"**Jarak dari Titik {titik_P_label} ke Garis {garis_AB_label}**.")
        st.markdown("Rumus: Proyeksi Titik ke Garis (Panjang garis tegak lurus).")
        st.latex("Jarak = \\frac{\\|\\vec{AP} \\times \\vec{AB}\\|}{\\|\\vec{AB}\\|}")
        st.latex(f"Jarak = {jarak_val:.2f}")

        st.info(f"Jarak Titik {titik_P_label} ke Garis {garis_AB_label} adalah **{jarak_val:.2f}** satuan.")

    with col_plot:
        # Visualisasi Titik ke Garis: Highlight titik, garis, dan garis tegak lurus (perlu vektor proyeksi)
        # Menghitung titik proyeksi Q pada garis AB
        t = np.dot(vec_AP, vec_AB) / np.dot(vec_AB, vec_AB)
        Q = np.array(A) + t * vec_AB

        fig_tg = buat_plot_kubus(sisi, highlight_points=[titik_P_label, A_label, B_label], highlight_line=[P, Q])
        st.plotly_chart(fig_tg, use_container_width=True)

elif pilihan_jarak == "Jarak Titik ke Bidang":
    
    # Simplifikasi: Jarak Titik ke Bidang (Alas/Atas/Samping)
    titik_P_label = st.sidebar.selectbox("Titik P:", ['G', 'E', 'D', 'B'])
    bidang_label = st.sidebar.selectbox("Bidang:", ['ABCD', 'EFGH', 'ABFE'])
    
    # Logika sederhana: Kubus simetris
    # Jarak Titik ke Bidang = Rusuk (jika titik tidak pada bidang, dan bidang sejajar sumbu)
    
    jarak_val = 0.0
    if titik_P_label in ['E', 'F', 'G', 'H'] and bidang_label == 'ABCD':
        jarak_val = sisi
        
    elif titik_P_label in ['A', 'B', 'C', 'D'] and bidang_label == 'EFGH':
        jarak_val = sisi
        
    elif titik_P_label in ['C', 'D', 'G', 'H'] and bidang_label == 'ABFE':
        jarak_val = sisi
        
    else:
        # Jika titik berada pada bidang (misal A ke ABCD), jaraknya 0
        if titik_P_label in list(bidang_label):
            jarak_val = 0.0
        else:
             # Jarak yang lebih kompleks (misalnya Titik E ke Bidang BGD)
             # Kita batasi pada kasus sederhana untuk menghindari kompleksitas berlebih.
             jarak_val = "Cek kasus sederhana/kompleks"
        

    with col_info:
        st.subheader("3. Jarak Titik ke Bidang")
        st.markdown(f"**Jarak dari Titik {titik_P_label} ke Bidang {bidang_label}**.")
        st.markdown("Pada kubus dengan kasus sederhana (bidang sejajar), jaraknya adalah panjang rusuk.")
        
        st.latex(f"Jarak = {jarak_val}")

        st.info(f"Jarak Titik {titik_P_label} ke Bidang {bidang_label} adalah **{jarak_val}** satuan.")

    with col_plot:
        # Visualisasi Titik ke Bidang: Highlight titik dan bidang
        fig_tb = buat_plot_kubus(sisi, highlight_points=[titik_P_label])
        
        # Highlight Bidang (Bidang ABCD: titik 0,1,2,3)
        # (Perlu menambahkan Mesh3d untuk bidang yang di-highlight)
        
        # Tambahkan fungsi highlight bidang yang lebih spesifik
        x_indices = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
        bidang_map = {
            'ABCD': [0, 1, 2, 3], 'EFGH': [4, 5, 6, 7], 
            'ABFE': [0, 1, 5, 4], 'BCGF': [1, 2, 6, 5],
            'CDHG': [2, 3, 7, 6], 'ADHE': [3, 0, 4, 7]
        }
        
        if bidang_label in bidang_map:
            i, j, k, l = bidang_map[bidang_label]
            fig_tb.add_trace(go.Mesh3d(
                x=[0, sisi, sisi, 0, 0, sisi, sisi, 0], y=[0, 0, sisi, sisi, 0, 0, sisi, sisi], z=[0, 0, 0, 0, sisi, sisi, sisi, sisi], 
                i=[i], j=[j], k=[k], opacity=0.5, color='green', name=bidang_label
            ))

        st.plotly_chart(fig_tb, use_container_width=True)

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info("Aplikasi menggunakan Plotly untuk visualisasi 3D interaktif.")
