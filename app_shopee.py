import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Shopee Affiliate Filter", layout="wide")

st.title("🛒 Pencari Produk Shopee Terlaris")
st.write("Saring produk berdasarkan kategori dan penjualan terbanyak, lalu *copy* link-nya untuk dijadikan tautan Affiliate Anda!")

# --- FUNGSI DATA SIMULASI ---
@st.cache_data
def load_dummy_data():
    data = {
        "Nama Produk": [
            "Sepatu Sneakers Pria", "Kemeja Flanel Kotak", "Headset Bluetooth TWS", 
            "Botol Minum 2 Liter", "Skincare Serum Wajah", "Panci Set Anti Lengket",
            "Kopi Bubuk Arabica 1kg", "Keripik Kaca Pedas Gila"
        ],
        "Kategori": [
            "Fashion Pria", "Fashion Pria", "Elektronik", 
            "Rumah Tangga", "Kecantikan", "Rumah Tangga",
            "Makanan dan Minuman", "Makanan dan Minuman"
        ],
        "Terjual / Bulan": [1200, 850, 3000, 5000, 2500, 400, 2100, 5000],
        "Komisi (%)": [5, 10, 8, 12, 15, 5, 10, 12],
        "Link Produk": [
            "https://shopee.co.id/sepatu-sneakers-contoh",
            "https://shopee.co.id/kemeja-flanel-contoh",
            "https://shopee.co.id/headset-tws-contoh",
            "https://shopee.co.id/botol-minum-contoh",
            "https://shopee.co.id/skincare-serum-contoh",
            "https://shopee.co.id/panci-set-contoh",
            "https://shopee.co.id/kopi-arabica-contoh",
            "https://shopee.co.id/keripik-kaca-contoh"
        ]
    }
    df = pd.DataFrame(data)
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

# 2. Filter Jumlah Terjual Minimal
min_terjual = st.sidebar.number_input("Minimal Produk Terjual (Pieces)", min_value=0, value=1000, step=100)

# --- PROSES PENYARINGAN ---
# Terapkan filter kategori dan jumlah terjual
df_filtered = df[
    (df["Kategori"].isin(pilih_kategori)) & 
    (df["Terjual / Bulan"] >= min_terjual)
]

# KUNCI UTAMA: Urutkan otomatis berdasarkan "Terjual / Bulan" paling banyak ke paling sedikit
df_filtered = df_filtered.sort_values(by="Terjual / Bulan", ascending=False)

# --- TAMPILAN HASIL ---
st.subheader(f"📊 {len(df_filtered)} Produk Terlaris Sesuai Filter")

if not df_filtered.empty:
    # Menampilkan tabel interaktif
    st.dataframe(
        df_filtered,
        column_config={
            "Terjual / Bulan": st.column_config.NumberColumn(format="%d Pcs 📈"),
            "Komisi (%)": st.column_config.ProgressColumn(format="%d%%", min_value=0, max_value=20),
            # Membuat kolom link menjadi URL yang bisa di-klik dan di-copy dengan mudah
            "Link Produk": st.column_config.LinkColumn("🔗 Link Produk (Copy/Klik)")
        },
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    st.write("💡 **Cara *Copy* Link:** Arahkan kursor (*mouse*) ke sel link yang Anda inginkan, klik ikon *copy* kecil yang muncul, atau klik kanan dan pilih *Copy Link Address*.")
else:
    st.warning("Tidak ada produk yang memenuhi kriteria filter Anda. Coba turunkan standar jumlah terjual.")
