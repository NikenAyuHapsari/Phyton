import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

# --- A. Fungsi Bantu Matriks (Ditinggalkan untuk efisiensi, asumsikan sama) ---
# ... (Fungsi to_homogeneous, apply_matrix_transform, translasi, rotasi, refleksi, dilatasi, dan parse_titik dipertahankan dari versi sebelumnya)
# PASTIKAN SEMUA FUNGSI TRANSFORMASI DARI VERSI SEBELUMNYA ADA DI SINI.

def to_homogeneous(points):
    """Mengubah array titik (2, N) menjadi koordinat homogen (3, N)"""
    if points.ndim != 2 or points.shape[0] != 2:
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
        return points 

# --- B. Fungsi Transformasi (Dipertahankan dari versi sebelumnya) ---
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
# --- C. Fungsi Parsing Input dan D. Fungsi Plotting (Dipertahankan dari versi sebelumnya) ---
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
    
    if points_mat.shape[1] > 1:
        points_closed = np.hstack((points_mat, points_mat[:, 0].reshape(-1, 1)))
    else:
        points_closed = points_mat
        
    return points_closed, None

def plot_transformasi(titik_awal_mat, titik_akhir_mat, nama_transformasi):
    """Membuat plot interaktif untuk bangun datar/garis."""
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    
    all_points = np.hstack((titik_awal_mat, titik_akhir_mat))
    if all_points.size > 0:
        batas_min = np.floor(all_points.min() - 2)
        batas_max = np.ceil(all_points.max() + 2)
        ax.set_xlim(batas_min, batas_max)
        ax.set_ylim(batas_min, batas_max)
    
    # Plot Bangun/Garis Awal
    if titik_awal_mat.shape[1] > 2:
        ax.fill(titik_awal_mat[0, :-1], titik_awal_mat[1, :-1], 'blue', alpha=0.3, label='Bangun Awal')
    ax.plot(titik_awal_mat[0, :], titik_awal_mat[1, :], 'b--', linewidth=1, marker='o', markersize=5, label='Bangun Awal')
    
    # Plot Hasil Transformasi
    if titik_akhir_mat.shape[1] > 2:
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

st.set_page_config(layout="wide")
st.title("🔬 Virtual Lab Transformasi Geometri")
st.markdown("Pilih jenis transformasi menggunakan **Tab** di bawah.")

# --- Bagian Input dan Output Utama ---
col_input, col_output = st.columns([1, 1])

with col_input:
    st.header("1️⃣ Definisi Bangun Awal")
    st.markdown("**Format:** `x1,y1; x2,y2; ...`")
    
    default_coord = "1,1; 4,1; 4,3" 
    titik_str = st.text_area(
        "Simpul Bangun (Pisahkan dengan Titik Koma ';'):", 
        value=default_coord, 
        height=100
    )
    
    titik_awal_mat_closed, error_msg = parse_titik(titik_str)
    
    if error_msg:
        st.error(error_msg)
        st.stop()
    
    titik_awal_mat_open = titik_awal_mat_closed[:2, :-1] if titik_awal_mat_closed.shape[1] > 1 else titik_awal_mat_closed
    
    st.success(f"Ditemukan {titik_awal_mat_open.shape[1]} simpul.")
    
    df_awal = pd.DataFrame(titik_awal_mat_open.T, columns=['X', 'Y'])
    df_awal.index = [f'Simpul {i+1}' for i in range(df_awal.shape[0])]
    with st.expander("Lihat Koordinat Awal (Tabel)"):
        st.dataframe(df_awal)
        
    st.header("2️⃣ Parameter Transformasi")
    
    tab_trans, tab_rot, tab_dil, tab_ref = st.tabs(["Translasi", "Rotasi", "Dilatasi", "Refleksi"])
    
    # Inisialisasi parameter di luar tab untuk memastikan semua terbaca
    tx, ty = 0.0, 0.0
    sudut, rot_cx, rot_cy = 0, 0.0, 0.0
    skala, dil_cx, dil_cy = 1.0, 0.0, 0.0
    sumbu_refleksi = 'Sumbu X'
    
    # Variabel untuk melacak tab mana yang terakhir diubah (diperlukan untuk menentukan nama transformasi)
    # Kita menggunakan st.session_state untuk melacak tab aktif
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Translasi"

    with tab_trans:
        st.subheader("Translasi (Pergeseran)")
        # Menambahkan on_change callback dan state update
        if st.slider("Vektor X (tx)", -5.0, 5.0, 2.0, 0.1, key='tx', on_change=lambda: st.session_state.__setitem__('active_tab', "Translasi")):
            tx = st.session_state.tx
        if st.slider("Vektor Y (ty)", -5.0, 5.0, 1.0, 0.1, key='ty', on_change=lambda: st.session_state.__setitem__('active_tab', "Translasi")):
            ty = st.session_state.ty
        if 'tx' in st.session_state: tx = st.session_state.tx
        if 'ty' in st.session_state: ty = st.session_state.ty

    with tab_rot:
        st.subheader("Rotasi (Perputaran)")
        if st.slider("Sudut Rotasi (°)", -360, 360, 90, key='sudut', on_change=lambda: st.session_state.__setitem__('active_tab', "Rotasi")):
            sudut = st.session_state.sudut
        if st.number_input("Pusat Rotasi X (cx)", value=0.0, key='rot_cx', on_change=lambda: st.session_state.__setitem__('active_tab', "Rotasi")):
            rot_cx = st.session_state.rot_cx
        if st.number_input("Pusat Rotasi Y (cy)", value=0.0, key='rot_cy', on_change=lambda: st.session_state.__setitem__('active_tab', "Rotasi")):
            rot_cy = st.session_state.rot_cy
        if 'sudut' in st.session_state: sudut = st.session_state.sudut
        if 'rot_cx' in st.session_state: rot_cx = st.session_state.rot_cx
        if 'rot_cy' in st.session_state: rot_cy = st.session_state.rot_cy

    with tab_dil:
        st.subheader("Dilatasi (Perkalian Skala)")
        if st.slider("Faktor Skala (k)", -3.0, 3.0, 2.0, 0.1, key='skala', on_change=lambda: st.session_state.__setitem__('active_tab', "Dilatasi")):
            skala = st.session_state.skala
        if st.number_input("Pusat Dilatasi X (cx)", value=0.0, key='dil_cx', on_change=lambda: st.session_state.__setitem__('active_tab', "Dilatasi")):
            dil_cx = st.session_state.dil_cx
        if st.number_input("Pusat Dilatasi Y (cy)", value=0.0, key='dil_cy', on_change=lambda: st.session_state.__setitem__('active_tab', "Dilatasi")):
            dil_cy = st.session_state.dil_cy
        if 'skala' in st.session_state: skala = st.session_state.skala
        if 'dil_cx' in st.session_state: dil_cx = st.session_state.dil_cx
        if 'dil_cy' in st.session_state: dil_cy = st.session_state.dil_cy

    with tab_ref:
        st.subheader("Refleksi (Pencerminan)")
        if st.selectbox("Sumbu atau Garis Refleksi:", ('Sumbu X', 'Sumbu Y', 'Garis y=x', 'Garis y=-x'), key='sumbu', on_change=lambda: st.session_state.__setitem__('active_tab', "Refleksi")):
            sumbu_refleksi = st.session_state.sumbu
        if 'sumbu' in st.session_state: sumbu_refleksi = st.session_state.sumbu
        
        map_sumbu = {'Sumbu X': 'x', 'Sumbu Y': 'y', 'Garis y=x': 'y=x', 'Garis y=-x': 'y=-x'}


# --- G. Logika Pemrosesan Transformasi Global ---

# Tentukan transformasi berdasarkan tab yang terakhir diubah (st.session_state.active_tab)
transformasi_nama = st.session_state.active_tab

if transformasi_nama == 'Translasi':
    titik_akhir_mat_open = translasi(titik_awal_mat_open, tx, ty)
elif transformasi_nama == 'Rotasi':
    titik_akhir_mat_open = rotasi(titik_awal_mat_open, sudut, rot_cx, rot_cy)
elif transformasi_nama == 'Dilatasi':
    titik_akhir_mat_open = dilatasi(titik_awal_mat_open, skala, dil_cx, dil_cy)
elif transformasi_nama == 'Refleksi':
    titik_akhir_mat_open = refleksi(titik_awal_mat_open, map_sumbu[sumbu_refleksi])
else:
    titik_akhir_mat_open = titik_awal_mat_open

# Penutupan Bangun Akhir untuk Plotting
if titik_akhir_mat_open.shape[1] > 1:
    titik_akhir_mat_closed = np.hstack((titik_akhir_mat_open, titik_akhir_mat_open[:, 0].reshape(-1, 1)))
else:
    titik_akhir_mat_closed = titik_akhir_mat_open


# --- F. Kolom Output ---
with col_output:
    st.header(f"3️⃣ Visualisasi {transformasi_nama}")
    
    if titik_awal_mat_closed is not None and titik_akhir_mat_closed is not None:
        plot_transformasi(titik_awal_mat_closed, titik_akhir_mat_closed, transformasi_nama)
        
    st.subheader("Tabel Koordinat Hasil Akhir (A')")
    df_akhir = pd.DataFrame(titik_akhir_mat_closed[:2, :-1].T, columns=['X\'', 'Y\''])
    df_akhir.index = [f'Simpul {i+1}' for i in range(df_akhir.shape[0])]
    with st.expander("Lihat Koordinat Akhir (Tabel)"):
        st.dataframe(df_akhir)

st.divider()
st.caption("Aplikasi ini menggunakan **st.session_state** dan *unique keys* untuk menyinkronkan grafik dengan tab yang terakhir diinteraksi.")
