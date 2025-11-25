import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- A. Fungsi Transformasi Geometri ---

def translasi(titik, tx, ty):
    """Melakukan Translasi (Pergeseran)"""
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]])
    titik_homogen = np.append(titik, 1)
    titik_baru_homogen = T @ titik_homogen
    return titik_baru_homogen[:2]

def rotasi(titik, sudut_deg, cx=0, cy=0):
    """Melakukan Rotasi terhadap titik pusat (cx, cy)"""
    sudut_rad = np.deg2rad(sudut_deg)
    
    # Matriks Rotasi
    R = np.array([[np.cos(sudut_rad), -np.sin(sudut_rad), 0],
                  [np.sin(sudut_rad), np.cos(sudut_rad), 0],
                  [0, 0, 1]])
    
    # Titik dalam koordinat homogen
    P_homogen = np.append(titik, 1)
    
    # 1. Translasi titik ke pusat (cx, cy) ke (0,0)
    T1 = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]])
    
    # 2. Rotasi
    # 3. Translasi kembali ke pusat (cx, cy)
    T2 = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]])
    
    # Transformasi gabungan
    M = T2 @ R @ T1
    
    titik_baru_homogen = M @ P_homogen
    return titik_baru_homogen[:2]

def refleksi(titik, sumbu):
    """Melakukan Refleksi terhadap sumbu x, y, atau garis y=x, y=-x"""
    x, y = titik
    if sumbu == 'x':
        return np.array([x, -y])
    elif sumbu == 'y':
        return np.array([-x, y])
    elif sumbu == 'y=x':
        return np.array([y, x])
    elif sumbu == 'y=-x':
        return np.array([-y, -x])
    return titik

def dilatasi(titik, skala, cx=0, cy=0):
    """Melakukan Dilatasi terhadap titik pusat (cx, cy)"""
    x, y = titik
    
    # 1. Translasi titik ke pusat (cx, cy) ke (0,0)
    xt = x - cx
    yt = y - cy
    
    # 2. Dilatasi
    xd = xt * skala
    yd = yt * skala
    
    # 3. Translasi kembali ke pusat (cx, cy)
    x_baru = xd + cx
    y_baru = yd + cy
    
    return np.array([x_baru, y_baru])

# --- B. Fungsi Plotting ---

def plot_transformasi(titik_awal, titik_akhir, nama_transformasi):
    """Membuat plot interaktif menggunakan Matplotlib."""
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Plot Titik Awal
    ax.plot(titik_awal[0], titik_awal[1], 'o-', label='Titik Awal (A)', color='blue')
    ax.text(titik_awal[0] + 0.2, titik_awal[1], f'A({titik_awal[0]:.1f}, {titik_awal[1]:.1f})', color='blue')

    # Plot Titik Akhir
    ax.plot(titik_akhir[0], titik_akhir[1], 'x--', label=f'Hasil {nama_transformasi} (A\')', color='red')
    ax.text(titik_akhir[0] + 0.2, titik_akhir[1], f"A'({titik_akhir[0]:.1f}, {titik_akhir[1]:.1f})", color='red')
    
    # Pengaturan Grid
    batas_min = min(titik_awal.min(), titik_akhir.min()) - 2
    batas_max = max(titik_awal.max(), titik_akhir.max()) + 2
    ax.set_xlim(batas_min, batas_max)
    ax.set_ylim(batas_min, batas_max)
    
    # Garis Sumbu X dan Y
    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(0, color='gray', linestyle='--')
    
    ax.set_xlabel('Sumbu X')
    ax.set_ylabel('Sumbu Y')
    ax.set_title(f"Visualisasi Transformasi: {nama_transformasi}")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


# --- C. Struktur Aplikasi Streamlit ---

st.set_page_config(layout="wide")

st.title("🔬 Virtual Lab Transformasi Geometri")
st.markdown("Interaksi langsung dengan slider dan input untuk memahami konsep **Translasi**, **Rotasi**, **Dilatasi**, dan **Refleksi**.")
st.divider()

# Input Koordinat Awal
st.header("1️⃣ Koordinat Titik Awal (A)")
col_x, col_y = st.columns(2)

with col_x:
    titik_x = st.slider("Koordinat X (Absis)", -10.0, 10.0, 3.0, 0.1)
with col_y:
    titik_y = st.slider("Koordinat Y (Ordinat)", -10.0, 10.0, 2.0, 0.1)

titik_awal = np.array([titik_x, titik_y])
st.info(f"Titik Awal: **A({titik_awal[0]:.1f}, {titik_awal[1]:.1f})**")

st.divider()

# Pilihan Transformasi
st.header("2️⃣ Pilih Jenis Transformasi")
transformasi_pilih = st.selectbox(
    "Pilih transformasi yang ingin Anda lakukan:",
    ('Translasi', 'Rotasi', 'Dilatasi', 'Refleksi')
)
st.divider()

# --- D. Logika Transformasi Berdasarkan Pilihan ---

titik_akhir = titik_awal

if transformasi_pilih == 'Translasi':
    st.subheader("Translasi (Pergeseran)")
    col_tx, col_ty = st.columns(2)
    with col_tx:
        tx = st.slider("Pergeseran pada Sumbu X (tx)", -5.0, 5.0, 2.0, 0.1)
    with col_ty:
        ty = st.slider("Pergeseran pada Sumbu Y (ty)", -5.0, 5.0, 1.0, 0.1)
    
    titik_akhir = translasi(titik_awal, tx, ty)
    st.success(f"Vektor Translasi: **T({tx:.1f}, {ty:.1f})**")

elif transformasi_pilih == 'Rotasi':
    st.subheader("Rotasi (Perputaran)")
    col_sudut, col_pusat = st.columns(2)
    with col_sudut:
        sudut = st.slider("Sudut Rotasi (Derajat)", -360, 360, 90)
    with col_pusat:
        pusat_x = st.number_input("Pusat Rotasi X (cx)", value=0.0)
        pusat_y = st.number_input("Pusat Rotasi Y (cy)", value=0.0)
        
    titik_akhir = rotasi(titik_awal, sudut, pusat_x, pusat_y)
    st.success(f"Rotasi **{sudut}°** terhadap pusat **P({pusat_x:.1f}, {pusat_y:.1f})**")

elif transformasi_pilih == 'Dilatasi':
    st.subheader("Dilatasi (Perkalian Skala)")
    col_skala, col_pusat = st.columns(2)
    with col_skala:
        skala = st.slider("Faktor Skala (k)", -3.0, 3.0, 2.0, 0.1)
    with col_pusat:
        pusat_x = st.number_input("Pusat Dilatasi X (cx)", value=0.0)
        pusat_y = st.number_input("Pusat Dilatasi Y (cy)", value=0.0)
        
    titik_akhir = dilatasi(titik_awal, skala, pusat_x, pusat_y)
    st.success(f"Dilatasi dengan faktor skala **k={skala:.1f}** terhadap pusat **P({pusat_x:.1f}, {pusat_y:.1f})**")

elif transformasi_pilih == 'Refleksi':
    st.subheader("Refleksi (Pencerminan)")
    sumbu_refleksi = st.selectbox(
        "Sumbu atau Garis Refleksi:",
        ('Sumbu X (y=0)', 'Sumbu Y (x=0)', 'Garis y=x', 'Garis y=-x'),
        format_func=lambda x: x.replace('Sumbu X (y=0)', 'Sumbu X').replace('Sumbu Y (x=0)', 'Sumbu Y')
    )
    
    # Mapping pilihan ke kunci fungsi
    map_sumbu = {'Sumbu X (y=0)': 'x', 'Sumbu Y (x=0)': 'y', 'Garis y=x': 'y=x', 'Garis y=-x': 'y=-x'}
    
    titik_akhir = refleksi(titik_awal, map_sumbu[sumbu_refleksi])
    st.success(f"Refleksi terhadap **{sumbu_refleksi}**")


# --- E. Visualisasi Hasil ---
st.header("3️⃣ Visualisasi Hasil Transformasi")

# Hitung dan Tampilkan Koordinat Akhir
if titik_awal.all() != titik_akhir.all():
     st.markdown(f"Titik **A'** (Hasil Transformasi): **({titik_akhir[0]:.1f}, {titik_akhir[1]:.1f})**")
else:
     st.markdown(f"Titik **A'** (Hasil Transformasi): **A({titik_akhir[0]:.1f}, {titik_akhir[1]:.1f})** (Sama dengan Awal)")

plot_transformasi(titik_awal, titik_akhir, transformasi_pilih)

st.divider()
st.caption("Dibuat dengan Python dan Streamlit. Interaksi visual memudahkan pemahaman konsep transformasi geometri.")
