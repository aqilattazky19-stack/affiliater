import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Shopee Affiliate Filter", layout="wide")

st.title("🛒 Pencari Komisi Shopee Affiliate Maksimal")
st.write("Temukan produk terlaris dengan komisi paling besar untuk dipromosikan.")

# --- FUNGSI DATA SIMULASI (Agar bisa langsung dites) ---
@st.cache_data
def # --- FUNGSI DATA SIMULASI ---
@st.cache_data
def load_dummy_data():
    data = {
        "Nama Produk": [
            "Sepatu Sneakers Pria", "Kemeja Flanel Kotak", "Headset Bluetooth TWS", 
            "Botol Minum 2 Liter", "Skincare Serum Wajah", "Panci Set Anti Lengket",
            "Kopi Bubuk Arabica 1kg", "Keripik Kaca Pedas Gila" # <--- Produk Baru
        ],
        "Kategori": [
            "Fashion Pria", "Fashion Pria", "Elektronik", 
            "Rumah Tangga", "Kecantikan", "Rumah Tangga",
            "Makanan dan Minuman", "Makanan dan Minuman" # <--- Kategori Baru
        ],
        "Harga (Rp)": [150000, 85000, 120000, 45000, 95000, 250000, 85000, 15000],
        "Terjual / Bulan": [1200, 850, 3000, 5000, 2500, 400, 2100, 5000],
        "Komisi (%)": [5, 10, 8, 12, 15, 5, 10, 12],
    }
    df = pd.DataFrame(data)
    df["Estimasi Komisi (Rp)"] = (df["Harga (Rp)"] * df["Komisi (%)"] / 100).astype(int)
    return df

# --- AREA UNGGAH DATA ---
st.sidebar.header("📁 Sumber Data")
uploaded_file = st.sidebar.file_uploader("Unggah Excel/CSV dari Dasbor Shopee", type=["csv", "xlsx"])

if uploaded_file:
    # Membaca data asli jika pengguna mengunggah file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.success("Data asli berhasil dimuat!")
else:
    # Menggunakan data simulasi jika belum ada file
    df = load_dummy_data()
    st.info("💡 Menampilkan Data Simulasi. Silakan unggah file dari Shopee Affiliate untuk data asli.")

# --- AREA FILTERING ---
st.sidebar.header("⚙️ Filter Produk")

# 1. Filter Kategori
kategori_unik = df["Kategori"].unique().tolist()
pilih_kategori = st.sidebar.multiselect("Pilih Kategori:", options=kategori_unik, default=kategori_unik)

# 2. Filter Komisi Minimal
min_komisi = st.sidebar.slider("Minimal Persentase Komisi (%)", min_value=0, max_value=20, value=5)

# 3. Filter Jumlah Terjual
min_terjual = st.sidebar.number_input("Minimal Produk Terjual (Pieces)", min_value=0, value=500, step=100)

# --- PROSES PENYARINGAN ---
# Terapkan filter ke dalam tabel data
df_filtered = df[
    (df["Kategori"].isin(pilih_kategori)) & 
    (df["Komisi (%)"] >= min_komisi) & 
    (df["Terjual / Bulan"] >= min_terjual)
]

# Urutkan berdasarkan Estimasi Komisi Rp tertinggi
df_filtered = df_filtered.sort_values(by="Estimasi Komisi (Rp)", ascending=False)

# --- TAMPILAN HASIL ---
st.subheader(f"📊 Menampilkan {len(df_filtered)} Produk Terbaik")

if not df_filtered.empty:
    # Menampilkan tabel interaktif
    st.dataframe(
        df_filtered,
        column_config={
            "Harga (Rp)": st.column_config.NumberColumn(format="Rp %d"),
            "Estimasi Komisi (Rp)": st.column_config.NumberColumn(format="Rp %d", help="Nominal yang didapat per 1 barang terjual"),
            "Komisi (%)": st.column_config.ProgressColumn(format="%d%%", min_value=0, max_value=20)
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Tidak ada produk yang memenuhi kriteria filter Anda. Coba turunkan standar komisi atau jumlah terjual.")
