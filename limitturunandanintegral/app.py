import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# --- Konfigurasi Halaman Utama ---
st.set_page_config(
    page_title="Virtual Lab Kalkulus (Limit, Turunan, Integral)",
    page_icon="📐",
    layout="wide"
)

st.title("📐 Virtual Lab: Kalkulus Dasar")
st.markdown("Eksplorasi interaktif **Limit**, **Turunan**, dan **Integral** dengan fungsi kustom.")

# Definisikan simbol x untuk SymPy
x = sp.Symbol('x')

# ----------------------------------------------------------------------
#                         SIDEBAR (INPUT - KIRI)
# ----------------------------------------------------------------------

st.sidebar.header("⚙️ Pengaturan Fungsi")

# Input Fungsi dari Pengguna
fungsi_str = st.sidebar.text_input(
    "Masukkan Fungsi $f(x)$ (Contoh: x**2 - 2*x + 1):",
    value="x**3 - 3*x**2 + 5"
)

try:
    f_x = sp.sympify(fungsi_str)
    # Konversi fungsi SymPy ke fungsi numerik untuk plotting
    f_num = sp.lambdify(x, f_x, 'numpy')
    st.sidebar.success(f"Fungsi $f(x)$ berhasil didefinisikan: ${sp.latex(f_x)}$")
except Exception as e:
    st.sidebar.error(f"⚠️ Error Input Fungsi: {e}. Pastikan menggunakan format Python yang benar (misalnya `x**2`).")
    st.stop() # Hentikan eksekusi jika input fungsi error

# Pilihan Topik
topik = st.sidebar.radio(
    "Pilih Topik Kalkulus:",
    ("Limit", "Turunan (Diferensial)", "Integral")
)

# Pengaturan Plotting
st.sidebar.subheader("Pengaturan Plot")
x_min = st.sidebar.number_input("Batas x minimum:", value=-4.0)
x_max = st.sidebar.number_input("Batas x maksimum:", value=4.0)


# ----------------------------------------------------------------------
#                         MAIN AREA (OUTPUT - KANAN)
# ----------------------------------------------------------------------

st.header(f"Analisis Fungsi: $f(x) = {sp.latex(f_x)}$")
st.markdown("---")

# Membuat rentang nilai x untuk plotting
x_vals = np.linspace(x_min, x_max, 500)
try:
    y_vals = f_num(x_vals)
except:
    st.error("Error saat menghitung nilai y. Cek rentang x atau fungsi Anda.")
    st.stop()


## 1. Plot Fungsi Utama (Selalu Tampil)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x_vals, y_vals, label=f'$f(x)$', color='blue')
ax.axhline(0, color='gray', linestyle='--')
ax.axvline(0, color='gray', linestyle='--')
ax.set_title(f"Grafik Fungsi: $f(x) = {sp.latex(f_x)}$", fontsize=16)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)

# Area untuk Plot dan Hasil (Layout Dua Kolom)
col_plot, col_result = st.columns([3, 2])

with col_plot:
    st.pyplot(fig) # Tampilkan plot dasar

with col_result:
    st.subheader("Hasil Perhitungan")

    if topik == "Limit":
        st.subheader("🔬 Limit Fungsi")
        a_limit = st.number_input("Hitung Limit saat $x \\to a$, masukkan nilai $a$:", value=1.0)
        
        # Perhitungan Limit SymPy
        limit_val = sp.limit(f_x, x, a_limit)
        
        st.latex(f"\\lim_{{x \\to {a_limit}}} f(x) = \\lim_{{x \\to {a_limit}}} ({sp.latex(f_x)}) = {sp.latex(limit_val)}")
        
        st.info(f"Nilai Limit adalah **{limit_val}**.")
        
        # Tambahkan visualisasi titik limit pada plot
        with col_plot:
            try:
                # Plot titik limit jika hasilnya bukan tak terhingga
                if limit_val != sp.oo and limit_val != -sp.oo:
                    ax.plot(a_limit, limit_val, 'ro', label=f'Limit ({a_limit}, {limit_val})')
                    ax.annotate(f"({a_limit}, {limit_val})", (a_limit, limit_val), textcoords="offset points", xytext=(5,5), ha='center')
                    ax.legend()
                    st.pyplot(fig)
            except:
                pass # Abaikan jika terjadi error plotting limit tak terhingga
                

    elif topik == "Turunan (Diferensial)":
        st.subheader("📈 Turunan Fungsi")
        
        # Perhitungan Turunan SymPy
        turunan_f = sp.diff(f_x, x)
        
        st.latex(f"f'(x) = \\frac{{d}}{{dx}} ({sp.latex(f_x)}) = {sp.latex(turunan_f)}")
        
        # Hitung nilai turunan pada titik tertentu
        a_turunan = st.number_input("Hitung $f'(a)$, masukkan nilai $a$:", value=1.0)
        turunan_num = sp.lambdify(x, turunan_f, 'numpy')
        nilai_turunan = turunan_num(a_turunan)
        nilai_f_a = f_num(a_turunan)
        
        st.latex(f"f'({a_turunan}) = {nilai_turunan:,.4f}")
        st.info(f"Nilai turunan (gradien garis singgung) pada $x={a_turunan}$ adalah **{nilai_turunan:,.4f}**.")
        
        # Visualisasi Turunan (Garis Singgung)
        with col_plot:
            # Garis singgung: y - f(a) = f'(a) * (x - a)
            tangent_line = nilai_turunan * (x_vals - a_turunan) + nilai_f_a
            
            # Plot titik dan garis singgung
            ax.plot(a_turunan, nilai_f_a, 'go', label=f'Titik ({a_turunan}, {nilai_f_a:,.2f})')
            ax.plot(x_vals, tangent_line, 'g--', label='Garis Singgung')
            ax.legend()
            st.pyplot(fig)
            # 

    elif topik == "Integral":
        st.subheader("🧮 Integral Tentu")
        
        # Input Batas Integral
        a_integral = st.number_input("Batas Bawah ($a$):", value=0.0)
        b_integral = st.number_input("Batas Atas ($b$):", value=2.0)
        
        # Perhitungan Integral Tentu SymPy
        integral_val = sp.integrate(f_x, (x, a_integral, b_integral))
        
        st.latex(f"\\int_{{{a_integral}}}^{{{b_integral}}} f(x) dx = \\int_{{{a_integral}}}^{{{b_integral}}} ({sp.latex(f_x)}) dx = {sp.latex(integral_val)}")
        
        st.info(f"Nilai Integral Tentu (Luas Area) adalah **{integral_val:,.4f}**.")
        
        # Visualisasi Integral (Area di Bawah Kurva)
        with col_plot:
            # Cari indeks x untuk batas integral
            idx_a = np.argmin(np.abs(x_vals - a_integral))
            idx_b = np.argmin(np.abs(x_vals - b_integral))
            
            # Ambil segmen kurva
            x_area = x_vals[idx_a:idx_b+1]
            y_area = y_vals[idx_a:idx_b+1]
            
            # Isi area di bawah kurva
            ax.fill_between(x_area, 0, y_area, color='orange', alpha=0.3, label='Area Integral')
            ax.legend()
            st.pyplot(fig)
            # 
            
# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info("Aplikasi menggunakan SymPy untuk kalkulasi simbolik dan Matplotlib untuk visualisasi.")
