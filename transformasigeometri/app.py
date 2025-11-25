import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

# --- A. Fungsi Bantu Matriks (Sama seperti sebelumnya) ---

def to_homogeneous(points):
    """Mengubah array titik (2, N) menjadi koordinat homogen (3, N)"""
    if points.ndim != 2 or points.shape[0] != 2:
        # Menangani kasus 1 titik jika inputnya tidak (2,1)
        if points.ndim == 1 and points.shape[0] == 2:
            points = points.reshape(2, 1)
        else:
            raise ValueError("Input harus array NumPy dengan shape (2, N)")
    ones = np.ones((1, points.shape[1]))
    return np.vstack((points, ones))

def apply_matrix_transform(points, matrix):
    """Menerapkan transformasi matriks pada semua titik."""
    try:
        points_h = to_homogeneous(points)
        transformed_h = matrix @ points_h
        return transformed_h[:2, :]
    except ValueError:
        # Tangani error jika input titik kosong atau tidak valid
        return points 

# --- B. Fungsi Transformasi (Sama seperti sebelumnya, disingkat untuk tampilan) ---

def translasi(points, tx, ty):
    T = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    return apply_matrix_transform(points, T)

def rotasi(points, sudut_deg, cx=0, cy=0):
    sudut_rad = np.deg2rad(sudut_deg)
    cos, sin = np.cos(sudut_rad), np.sin(sudut_rad)
    R = np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
    T1 = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]]) 
    T2 = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]])
    M = T2 @ R @ T1
    return apply_matrix_transform(points, M)

def refleksi(points, sumbu):
    if sumbu == 'x':
        M = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    elif sumbu == 'y':
        M = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
    elif sumbu == 'y=x':
        M = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    elif sumbu == 'y=-x':
        M = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, 1]])
    else:
        M = np.eye(3) 
    return apply_matrix_transform(points, M)

def dilatasi(points, skala, cx=0, cy=0):
    D = np.array([[skala, 0, 0], [0, skala, 0], [0, 0, 1]])
    T1 = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]]) 
    T2 = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]]) 
    M = T2 @ D @ T1
    return apply_matrix_transform(points, M)

# --- C. Fungsi Parsing Input ---

def parse_titik(titik_str):
    """Menguraikan string input menjadi matriks titik (2, N)"""
    points = []
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
    
    # Tambahkan titik pertama di akhir untuk menutup bangun (jika > 1 titik)
    if points_mat.shape[1] > 1:
        points_closed = np.hstack((points_mat, points_mat[:, 0].reshape(-1, 1)))
    else:
        points_closed = points_mat
        
    return points_closed, None

# --- D. Fungsi Plotting (Sama seperti sebelumnya) ---

def plot_transformasi(titik_awal_mat, titik_akhir_mat, nama_transformasi):
    """Membuat plot interaktif untuk bangun datar/garis."""
    fig, ax = plt.subplots(figsize=(6.5, 6.5)) # Ukuran disesuaikan untuk kolom
    
    # Tentukan batas plot
    all_points = np.hstack((titik_awal_mat, titik_akhir_mat))
    if all_points.size > 0:
        batas_min = np.floor(all_points.min() - 2)
        batas_max = np.ceil(all_points.max() + 2)
        ax.set_xlim(batas_min, batas_max)
        ax.set_ylim(batas_min, batas_max)
    
    # Plot Bangun/Garis Awal
    if titik_awal_mat.shape[1] > 2: # Bangun Datar
        ax.fill(titik_awal_mat[0, :-1], titik_awal_mat[1, :-1], 'blue', alpha=0.3, label='Bangun Awal')
    ax.plot(titik_awal_mat[0, :], titik_awal_mat[1, :], 'b--', linewidth=1, marker='o', markersize=5, label='Bangun Awal')
    
    # Plot Hasil Transformasi
    if titik_akhir_mat.shape[1] > 2: # Bangun Datar
        ax.fill(titik_akhir_mat[0, :-1], titik_akhir_mat[1, :-1], 'red', alpha=0.5, label='Bangun Akhir')
    ax.plot(titik_akhir_mat[0, :], titik_akhir_mat[1, :], 'r-', linewidth=2, marker='x', markersize=6, label=f'Hasil {nama_transformasi}')
    
    # Pengaturan Grid
    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(0, color='gray', linestyle='--')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('Sumbu X')
    ax.set_ylabel('Sumbu Y')
    ax.set_title(f"Visualisasi: {nama_transformasi}")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


# --- E. Struktur Aplikasi Streamlit Utama (Menggunakan Kolom dan Tabs) ---

# Mengatur layout halaman menjadi lebar penuh
st.set_page_config(layout="wide")

st.title("🔬 Virtual Lab Transformasi Geometri")
st.markdown("Pilih jenis transformasi menggunakan **Tab** di bawah.")

# --- Bagian Input dan Output Utama ---
col_input, col_output = st.columns([1, 1]) # Membagi layar menjadi 50% untuk Input dan 50% untuk Output

with col_input:
    st.header("1️⃣ Definisi Bangun Awal")
    st.markdown("**Format:** `x1,y1; x2,y2; ...`")
    
    default_coord = "1,1; 4,1; 4,3" 
    titik_str = st.text_area(
        "Simpul Bangun (Pisahkan dengan Titik Koma ';'):", 
        value=default_coord, 
        height=100
    )
    
    # Parse input
    titik_awal_mat_closed, error_msg = parse_titik(titik_str)
    
    if error_msg:
        st.error(error_msg)
        st.stop()
    
    # Ambil matriks titik tanpa penutup untuk diolah (shape 2, N)
    titik_awal_mat_open = titik_awal_mat_closed[:2, :-1] if titik_awal_mat_closed.shape[1] > 1 else titik_awal_mat_closed
    
    st.success(f"Ditemukan {titik_awal_mat_open.shape[1]} simpul.")
    
    # Tampilkan koordinat awal dalam tabel
    df_awal = pd.DataFrame(titik_awal_mat_open.T, columns=['X', 'Y'])
    df_awal.index = [f'Simpul {i+1}' for i in range(df_awal.shape[0])]
    with st.expander("Lihat Koordinat Awal (Tabel)"):
        st.dataframe(df_awal)
        
    st.header("2️⃣ Parameter Transformasi")
    
    # --- Pengaturan Transformasi menggunakan Tabs ---
    tab_trans, tab_rot, tab_dil, tab_ref = st.tabs(["Translasi", "Rotasi", "Dilatasi", "Refleksi"])
    
    titik_akhir_mat = np.copy(titik_awal_mat_closed) # Inisialisasi
    transformasi_nama = ""

    with tab_trans:
        st.subheader("Translasi (Pergeseran)")
        tx = st.slider("Vektor X (tx)", -5.0, 5.0, 2.0, 0.1, key='tx')
        ty = st.slider("Vektor Y (ty)", -5.0, 5.0, 1.0, 0.1, key='ty')
        titik_akhir_mat = translasi(titik_awal_mat_open, tx, ty)
        transformasi_nama = "Translasi"

    with tab_rot:
        st.subheader("Rotasi (Perputaran)")
        sudut = st.slider("Sudut Rotasi (°)", -360, 360, 90, key='sudut')
        pusat_x = st.number_input("Pusat Rotasi X (cx)", value=0.0, key='rot_cx')
        pusat_y = st.number_input("Pusat Rotasi Y (cy)", value=0.0, key='rot_cy')
        titik_akhir_mat = rotasi(titik_awal_mat_open, sudut, pusat_x, pusat_y)
        transformasi_nama = "Rotasi"

    with tab_dil:
        st.subheader("Dilatasi (Perkalian Skala)")
        skala = st.slider("Faktor Skala (k)", -3.0, 3.0, 2.0, 0.1, key='skala')
        pusat_x = st.number_input("Pusat Dilatasi X (cx)", value=0.0, key='dil_cx')
        pusat_y = st.number_input("Pusat Dilatasi Y (cy)", value=0.0, key='dil_cy')
        titik_akhir_mat = dilatasi(titik_awal_mat_open, skala, pusat_x, pusat_y)
        transformasi_nama = "Dilatasi"

    with tab_ref:
        st.subheader("Refleksi (Pencerminan)")
        sumbu_refleksi = st.selectbox(
            "Sumbu atau Garis Refleksi:",
            ('Sumbu X', 'Sumbu Y', 'Garis y=x', 'Garis y=-x'),
            key='sumbu'
        )
        map_sumbu = {'Sumbu X': 'x', 'Sumbu Y': 'y', 'Garis y=x': 'y=x', 'Garis y=-x': 'y=-x'}
        titik_akhir_mat = refleksi(titik_awal_mat_open, map_sumbu[sumbu_refleksi])
        transformasi_nama = "Refleksi"

    # Penutupan Bangun Akhir untuk Plotting
    if titik_akhir_mat.shape[1] > 1:
        titik_akhir_mat_closed = np.hstack((titik_akhir_mat, titik_akhir_mat[:, 0].reshape(-1, 1)))
    else:
        titik_akhir_mat_closed = titik_akhir_mat

with col_output:
    st.header(f"3️⃣ Visualisasi {transformasi_nama}")
    
    # Menjalankan Plot
    if titik_awal_mat_closed is not None and titik_akhir_mat_closed is not None:
        plot_transformasi(titik_awal_mat_closed, titik_akhir_mat_closed, transformasi_nama)
        
    st.subheader("Tabel Koordinat Hasil Akhir (A')")
    # Membuat DataFrame untuk titik akhir
    df_akhir = pd.DataFrame(titik_akhir_mat_closed[:2, :-1].T, columns=['X\'', 'Y\''])
    df_akhir.index = [f'Simpul {i+1}' for i in range(df_akhir.shape[0])]
    with st.expander("Lihat Koordinat Akhir (Tabel)"):
        st.dataframe(df_akhir)

st.divider()
st.caption("Aplikasi ini menggunakan **st.columns** untuk tata letak 50/50 dan **st.tabs** untuk navigasi transformasi.")
