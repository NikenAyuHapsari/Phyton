import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
# ... (Semua fungsi transformasi, parsing, dan plotting dipertahankan) ...

# --- E. Struktur Aplikasi Streamlit Utama ---

st.set_page_config(layout="wide")
st.title("🔬 Virtual Lab Transformasi Geometri")
st.markdown("Pilih jenis transformasi menggunakan **Tab** di bawah.")

# --- Bagian Input dan Output Utama ---
col_input, col_output = st.columns([1, 1])

# --- Logika Callback untuk Tombol Submit ---
def handle_submit_coords(titik_str):
    """Fungsi callback untuk memproses input koordinat."""
    titik_awal_mat_closed, error_msg = parse_titik(titik_str)
    
    if error_msg:
        st.session_state.coord_error = error_msg
        st.session_state.titik_awal_mat_closed = None
    else:
        st.session_state.coord_error = None
        st.session_state.titik_awal_mat_closed = titik_awal_mat_closed
        # Reset tab aktif ke Translasi setelah input baru
        st.session_state.active_tab = "Translasi" 
        # Inisialisasi parameter default jika diperlukan (opsional)

# --- F. Kolom Input ---
with col_input:
    st.header("1️⃣ Definisi Bangun Awal")
    st.markdown("**Petunjuk:** Masukkan koordinat simpul dalam format `x1,y1; x2,y2; ...`")
    
    default_coord = "1,1; 4,1; 4,3" 
    
    # 1. Kotak teks area tanpa langsung memicu state
    titik_str_input = st.text_area(
        "Simpul Bangun (Pisahkan dengan Titik Koma ';'):", 
        value=default_coord, 
        height=100,
        key='raw_coords' # Key untuk menyimpan input mentah
    )
    
    # 2. Tombol Submit untuk memproses input
    st.button("✅ Submit & Perbarui Koordinat", 
              on_click=handle_submit_coords, 
              args=(titik_str_input,))
    
    # Inisialisasi session state jika belum ada
    if 'titik_awal_mat_closed' not in st.session_state:
        # Panggil fungsi parsing inisial
        handle_submit_coords(default_coord)

    # Ambil data dari session state
    titik_awal_mat_closed = st.session_state.titik_awal_mat_closed
    
    if st.session_state.coord_error:
        st.error(st.session_state.coord_error)
        st.stop()
    
    titik_awal_mat_open = titik_awal_mat_closed[:2, :-1] if titik_awal_mat_closed.shape[1] > 1 else titik_awal_mat_closed
    
    st.success(f"Ditemukan {titik_awal_mat_open.shape[1]} simpul.")
    
    # ... (Tabel Koordinat Awal Expander dipertahankan) ...
    df_awal = pd.DataFrame(titik_awal_mat_open.T, columns=['X', 'Y'])
    df_awal.index = [f'Simpul {i+1}' for i in range(df_awal.shape[0])]
    with st.expander("Lihat Koordinat Awal (Tabel)"):
        st.dataframe(df_awal)
        
    st.header("2️⃣ Parameter Transformasi")
    
    # --- Pengaturan Transformasi menggunakan Tabs (dipertahankan) ---
    tab_trans, tab_rot, tab_dil, tab_ref = st.tabs(["Translasi", "Rotasi", "Dilatasi", "Refleksi"])
    
    # ... (Logika Tabs dan widget input dipertahankan dengan KEY dan on_change callback) ...

    # Inisialisasi parameter di luar tab untuk memastikan semua terbaca
    # (Dipertahankan dari versi sebelumnya, pastikan semua variabel default terinisialisasi)
    tx, ty = 0.0, 0.0
    sudut, rot_cx, rot_cy = 0, 0.0, 0.0
    skala, dil_cx, dil_cy = 1.0, 0.0, 0.0
    sumbu_refleksi = 'Sumbu X'

    # Inisialisasi st.session_state.active_tab
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Translasi"

    # --- Logika Widget Tabs (Hanya Contoh Rotasi, yang lain sama) ---
    with tab_rot:
        st.subheader("Rotasi (Perputaran)")
        # Contoh: Widget di dalam tab menggunakan key unik
        sudut_value = st.slider("Sudut Rotasi (°)", -360, 360, 90, key='sudut', on_change=lambda: st.session_state.__setitem__('active_tab', "Rotasi"))
        rot_cx_value = st.number_input("Pusat Rotasi X (cx)", value=0.0, key='rot_cx', on_change=lambda: st.session_state.__setitem__('active_tab', "Rotasi"))
        rot_cy_value = st.number_input("Pusat Rotasi Y (cy)", value=0.0, key='rot_cy', on_change=lambda: st.session_state.__setitem__('active_tab', "Rotasi"))
        
    # --- Setelah Tabs: Ambil nilai terakhir yang diinteraksi dari session_state ---
    # Jika key ada di state, gunakan nilainya; jika tidak, gunakan nilai default widget.
    if 'tx' in st.session_state: tx = st.session_state.tx
    if 'ty' in st.session_state: ty = st.session_state.ty
    if 'sudut' in st.session_state: sudut = st.session_state.sudut
    if 'rot_cx' in st.session_state: rot_cx = st.session_state.rot_cx
    if 'rot_cy' in st.session_state: rot_cy = st.session_state.rot_cy
    if 'skala' in st.session_state: skala = st.session_state.skala
    if 'dil_cx' in st.session_state: dil_cx = st.session_state.dil_cx
    if 'dil_cy' in st.session_state: dil_cy = st.session_state.dil_cy
    if 'sumbu' in st.session_state: sumbu_refleksi = st.session_state.sumbu
    map_sumbu = {'Sumbu X': 'x', 'Sumbu Y': 'y', 'Garis y=x': 'y=x', 'Garis y=-x': 'y=-x'}
    
    
# --- G. Logika Pemrosesan Transformasi Global (Menggunakan data dari Session State) ---

transformasi_nama = st.session_state.active_tab

if transformasi_nama == 'Translasi':
    titik_akhir_mat_open = translasi(titik_awal_mat_open, tx, ty)
# ... (Logika elif lainnya dipertahankan) ...
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


# --- F. Kolom Output (dipertahankan) ---
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
st.caption("Aplikasi ini sekarang menggunakan tombol submit untuk menyinkronkan input koordinat.")
