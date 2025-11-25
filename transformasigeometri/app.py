import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd # Digunakan untuk menampilkan tabel koordinat

# --- A. Fungsi Bantu Matriks ---

def to_homogeneous(points):
    """Mengubah array titik (2, N) menjadi koordinat homogen (3, N)"""
    # Memastikan input dalam format (2, N)
    if points.ndim != 2 or points.shape[0] != 2:
        raise ValueError("Input harus array NumPy dengan shape (2, N)")
    
    # Tambahkan baris 1 di bawah untuk koordinat homogen
    ones = np.ones((1, points.shape[1]))
    return np.vstack((points, ones))

def apply_matrix_transform(points, matrix):
    """Menerapkan transformasi matriks pada semua titik."""
    # 1. Ubah ke homogen (3, N)
    points_h = to_homogeneous(points)
    
    # 2. Terapkan transformasi (Matriks 3x3 @ Titik 3xN)
    transformed_h = matrix @ points_h
    
    # 3. Ubah kembali ke koordinat kartesius (2, N)
    return transformed_h[:2, :]

# --- B. Fungsi Transformasi Geometri (Vectorized) ---

def translasi(points, tx, ty):
    """Matriks Translasi"""
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]])
    return apply_matrix_transform(points, T)

def rotasi(points, sudut_deg, cx=0, cy=0):
    """Matriks Rotasi terhadap pusat (cx, cy)"""
    sudut_rad = np.deg2rad(sudut_deg)
    cos = np.cos(sudut_rad)
    sin = np.sin(sudut_rad)
    
    # Matriks Rotasi terhadap (0,0)
    R = np.array([[cos, -sin, 0],
                  [sin, cos, 0],
                  [0, 0, 1]])
    
    # Matriks Translasi ke pusat rotasi
    T1 = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]]) # Ke (0,0)
    T2 = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]])  # Kembali ke (cx,cy)
    
    # Matriks Transformasi Gabungan: T2 * R * T1
    M = T2 @ R @ T1
    return apply_matrix_transform(points, M)

def refleksi(points, sumbu):
    """Matriks Refleksi"""
    if sumbu == 'x':
        M = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    elif sumbu == 'y':
        M = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
    elif sumbu == 'y=x':
        M = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    elif sumbu == 'y=-x':
        M = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, 1]])
    else: # Default identity
        M = np.eye(3) 
        
    return apply_matrix_transform(points, M)

def dilatasi(points, skala, cx=0, cy=0):
    """Matriks Dilatasi terhadap pusat (cx, cy)"""
    
    # Matriks Dilatasi terhadap (0,0)
    D = np.array([[skala, 0, 0],
                  [0, skala, 0],
                  [0, 0, 1]])
    
    # Matriks Translasi ke pusat dilatasi
    T1 = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]]) # Ke (0,0)
    T2 = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]])  # Kembali ke (cx,cy)
    
    # Matriks Transformasi Gabungan: T2 * D * T1
    M = T2 @ D @ T1
    return apply_matrix_transform(points, M)

# --- C. Fungsi Parsing Input ---

def parse_titik(titik_str):
    """Menguraikan string input menjadi matriks titik (2, N)"""
    points = []
    # Bersihkan string dari spasi dan pisahkan berdasarkan titik koma
    for pair in titik_str.replace(' ', '').split(';'):
        if ',' in pair:
            try:
                x, y = map(float, pair.split(','))
                points.append([x, y])
            except ValueError:
                continue
    
    if not points:
        return None, "Masukkan minimal satu pasang koordinat (format: x,y)."

    points_mat = np.array(points).T # Shape (2, N)
    
    # Untuk plotting, tambahkan titik pertama di akhir untuk menutup bangun (jika > 1 titik)
    if points_mat.shape[1] > 1:
        points_closed = np.hstack((points_mat, points_mat[:, 0].reshape(-1, 1)))
    else:
        # Untuk kasus titik tunggal
        points_closed = points_mat
        
    return points_closed, None # Shape (2, N_closed)

# --- D. Fungsi Plotting ---

def plot_transformasi(titik_awal_mat, titik_akhir_mat, nama_transformasi):
    """Membuat plot interaktif untuk bangun datar/garis."""
    fig, ax = plt.subplots(figsize=(7, 7))
    
    # Tentukan batas plot
    all_points = np.hstack((titik_awal_mat, titik_akhir_mat))
    if all_points.size > 0:
        batas_min = np.floor(all_points.min() - 2)
        batas_max = np.ceil(all_points.max() + 2)
        ax.set_xlim(batas_min, batas_max)
        ax.set_ylim(batas_min, batas_max)
    
    # 1. Plot Bangun/Garis Awal
    if titik_awal_mat.shape[1] > 2: # Bangun Datar
        ax.fill(titik_awal_mat[0, :-1], titik_awal_mat[1, :-1], 'blue', alpha=0.3, label='Bangun Awal')
    ax.plot(titik_awal_mat[0, :], titik_awal_mat[1, :], 'b--', linewidth=1, marker='o', markersize=5, label='Bangun Awal (Garis)')
    
    # 2. Plot Hasil Transformasi
    if titik_akhir_mat.shape[1] > 2: # Bangun Datar
        ax.fill(titik_akhir_mat[0, :-1], titik_akhir_mat[1, :-1], 'red', alpha=0.5, label='Bangun Akhir')
    ax.plot(titik_akhir_mat[0, :], titik_akhir_mat[1, :], 'r-', linewidth=2, marker='x', markersize=6, label=f'Hasil {nama_transformasi} (Garis)')
    
    # Pengaturan Grid
    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(0, color='gray', linestyle='--')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('Sumbu X')
    ax.set_ylabel('Sumbu Y')
    ax.set_title(f"Visualisasi Transformasi: {nama_transformasi}")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


# --- E. Struktur Aplikasi Streamlit Utama ---

st.set_page_config(layout="wide")

st.title("🔬 Virtual Lab Transformasi Geometri (Bangun Datar)")
st.markdown("Interaksi langsung untuk memahami **Translasi**, **Rotasi**, **Dilatasi**, dan **Refleksi** pada bangun datar/garis.")
st.divider()

# Input Koordinat Awal
st.header("1️⃣ Koordinat Bangun Awal")
st.markdown("**Petunjuk:** Masukkan koordinat simpul dalam format `x1,y1; x2,y2; x3,y3...`")

# Default untuk segitiga
default_coord = "1,1; 4,1; 4,3" 
titik_str = st.text_area(
    "Simpul Bangun (Pisahkan dengan Titik Koma ';'):", 
    value=default_coord, 
    height=100
)

# Parse input
titik_awal_mat, error_msg = parse_titik(titik_str)

if error_msg:
    st.error(error_msg)
    st.stop()

st.success(f"Ditemukan {titik_awal_mat.shape[1] - 1} simpul untuk diolah.")
# Tampilkan koordinat awal dalam tabel
df_awal = pd.DataFrame(titik_awal_mat[:, :-1].T, columns=['X', 'Y'])
df_awal.index = [f'Simpul {i+1}' for i in range(df_awal.shape[0])]
st.dataframe(df_awal)

st.divider()

# Pilihan Transformasi
st.header("2️⃣ Pilih dan Atur Transformasi")
transformasi_pilih = st.selectbox(
    "Pilih jenis transformasi:",
    ('Translasi', 'Rotasi', 'Dilatasi', 'Refleksi')
)
st.divider()

# --- F. Logika Transformasi Berdasarkan Pilihan (Interaktif) ---

titik_akhir_mat = np.copy(titik_awal_mat) # Default: tidak berubah

if transformasi_pilih == 'Translasi':
    st.subheader("Translasi (Pergeseran)")
    col_tx, col_ty = st.columns(2)
    with col_tx:
        tx = st.slider("Vektor X (tx)", -5.0, 5.0, 2.0, 0.1)
    with col_ty:
        ty = st.slider("Vektor Y (ty)", -5.0, 5.0, 1.0, 0.1)
    
    titik_akhir_mat = translasi(titik_awal_mat[:2, :], tx, ty)
    st.info(f"Vektor Translasi: **T({tx:.1f}, {ty:.1f})**")

elif transformasi_pilih == 'Rotasi':
    st.subheader("Rotasi (Perputaran)")
    col_sudut, col_pusat = st.columns(2)
    with col_sudut:
        sudut = st.slider("Sudut Rotasi (Derajat)", -360, 360, 90)
    with col_pusat:
        pusat_x = st.number_input("Pusat Rotasi X (cx)", value=0.0)
        pusat_y = st.number_input("Pusat Rotasi Y (cy)", value=0.0)
        
    titik_akhir_mat = rotasi(titik_awal_mat[:2, :], sudut, pusat_x, pusat_y)
    st.info(f"Rotasi **{sudut}°** terhadap pusat **P({pusat_x:.1f}, {pusat_y:.1f})**")

elif transformasi_pilih == 'Dilatasi':
    st.subheader("Dilatasi (Perkalian Skala)")
    col_skala, col_pusat = st.columns(2)
    with col_skala:
        skala = st.slider("Faktor Skala (k)", -3.0, 3.0, 2.0, 0.1)
    with col_pusat:
        pusat_x = st.number_input("Pusat Dilatasi X (cx)", value=0.0)
        pusat_y = st.number_input("Pusat Dilatasi Y (cy)", value=0.0)
        
    titik_akhir_mat = dilatasi(titik_awal_mat[:2, :], skala, pusat_x, pusat_y)
    st.info(f"Dilatasi dengan faktor skala **k={skala:.1f}** terhadap pusat **P({pusat_x:.1f}, {pusat_y:.1f})**")

elif transformasi_pilih == 'Refleksi':
    st.subheader("Refleksi (Pencerminan)")
    sumbu_refleksi = st.selectbox(
        "Sumbu atau Garis Refleksi:",
        ('Sumbu X', 'Sumbu Y', 'Garis y=x', 'Garis y=-x')
    )
    
    # Mapping pilihan ke kunci fungsi
    map_sumbu = {'Sumbu X': 'x', 'Sumbu Y': 'y', 'Garis y=x': 'y=x', 'Garis y=-x': 'y=-x'}
    
    titik_akhir_mat = refleksi(titik_awal_mat[:2, :], map_sumbu[sumbu_refleksi])
    st.info(f"Refleksi terhadap **{sumbu_refleksi}**")


# --- G. Visualisasi Hasil ---
st.header("3️⃣ Visualisasi dan Hasil Akhir")

col_plot, col_tabel = st.columns(2)

with col_plot:
    plot_transformasi(titik_awal_mat, titik_akhir_mat, transformasi_pilih)
    
with col_tabel:
    st.subheader("Tabel Koordinat Hasil Transformasi (A')")
    # Membuat DataFrame untuk titik akhir
    df_akhir = pd.DataFrame(titik_akhir_mat[:2, :-1].T, columns=['X\'', 'Y\''])
    df_akhir.index = [f'Simpul {i+1}' for i in range(df_akhir.shape[0])]
    st.dataframe(df_akhir)

st.divider()
st.caption("Dibuat untuk tujuan edukasi. Penggunaan matriks koordinat homogen memastikan transformasi yang akurat.")
