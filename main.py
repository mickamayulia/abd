# Import library
import streamlit as st
import pandas as pd
from datetime import datetime

# Import fungsi dari config.py
from config import *

st.set_page_config(page_title="Dashboard Sales", layout="wide")

# =====================================================
# FUNGSI AMBIL DATA
# =====================================================

result_customers = view_customers()

df_customers = pd.DataFrame(result_customers, columns=[
    "customer_id", "name", "email", "phone", "address", "birthdate", 
])

result_view_products = view_products()

df_view_products = pd.DataFrame(result_view_products, columns=[
    "product_id", "name", "descriptions", "price", "stock", 
])

result_orders = view_orders_with_customers()

df_orders = pd.DataFrame(result_orders, columns=[
    "order_id", "order_date", "total_amount", "customer_name", "phone" 
])

result_details = view_order_details_with_info()

df_view_details = pd.DataFrame(result_details, columns=[
    "order_detail_id", "order_id", "order_date",
    "customer_id", "customer_name",
    "product_id", "product_name", "unit_price",
    "quantity", "subtotal", "order_total", "phone" 
])



# =====================================================
# UI Streamlit
# =====================================================

st.title("📊 Sales Dashboard")

menu = st.sidebar.selectbox(
    "Pilih Tabel",
    ["Customers", "Products", "Orders", "Order Details", "Visualisasi"]
)

# =====================================================
# 📁 CUSTOMERS
# =====================================================
if menu == "Customers":
    st.header("📁 Data Customers")

    data = view_customers()
    df = pd.DataFrame(data, columns=[
        "customer_id", "name", "email", "phone", "address", "birthdate"
    ])

    st.dataframe(df, use_container_width=True)



# =====================================================
# 📦 PRODUCTS
# =====================================================
elif menu == "Products":
    st.header("📦 Data Products")

    data = view_products()
    df = pd.DataFrame(data, columns=[
        "product_id", "name", "description", "price", "stock"
    ])

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Produk", df.shape[0])
    col2.metric("Total Stok", df["stock"].sum())
    col3.metric("Harga Rata-rata", f"{df['price'].mean():,.0f}")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇ Download CSV", data=csv, file_name="products.csv")



# =====================================================
# 📑 ORDERS
# =====================================================
elif menu == "Orders":
    st.header("📑 Data Orders")

    data = view_orders_with_customers()
    df = pd.DataFrame(data, columns=[
        "order_id", "order_date", "total_amount", "customer_name", "phone"
    ])

    df["order_date"] = pd.to_datetime(df["order_date"])

    st.subheader("Filter Tanggal")
    start_date = st.date_input("Dari", df["order_date"].min().date())
    end_date = st.date_input("Sampai", df["order_date"].max().date())

    df_filtered = df[
        (df["order_date"].dt.date >= start_date) &
        (df["order_date"].dt.date <= end_date)
    ]

    st.dataframe(df_filtered, use_container_width=True)

    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("⬇ Download CSV", data=csv, file_name="orders.csv")



# =====================================================
# 📄 ORDER DETAILS
# =====================================================
elif menu == "Order Details":
    st.header("📄 Detail Order")

    data = view_order_details_with_info()
    df = pd.DataFrame(data, columns=[
    "order_detail_id", "order_id", "order_date",
    "customer_id", "customer_name",
    "product_id", "product_name", "unit_price",
    "quantity", "subtotal", "order_total", "phone"
    ])

    customers = ["Semua"] + sorted(df["customer_name"].unique().tolist())
    pilih_customer = st.selectbox("Filter Customer", customers)

    if pilih_customer != "Semua":
        df = df[df["customer_name"] == pilih_customer]

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇ Download CSV", data=csv, file_name="order_details.csv")

elif menu == "Visualisasi":
    st.header("📊 Visualisasi Data Penjualan")

    # ============================
    # 1. DATA CUSTOMERS
    # ============================
    data_customers = view_customers()
    df_customers = pd.DataFrame(data_customers, columns=[
        "customer_id", "name", "email", "phone", "address", "birthdate"
    ])

    if not df_customers.empty:
        df_customers["birthdate"] = pd.to_datetime(df_customers["birthdate"])
        df_customers["Age"] = (datetime.now() - df_customers["birthdate"]).dt.days // 365

        # Distribusi usia
        st.subheader("👶 Distribusi Usia Pelanggan")
        st.bar_chart(df_customers["Age"].value_counts().sort_index())

        # Pelanggan per kota
        st.subheader("🏙️ Jumlah Pelanggan per Kota / Alamat")
        st.bar_chart(df_customers["address"].value_counts())

    st.markdown("---")

    # ============================
    # 2. PRODUK TERLARIS
    # ============================
    result_top = top_selling_products()

    if result_top:
        df_top = pd.DataFrame(result_top, columns=["product_name", "total_sold"])
        st.subheader("🥇 Produk Terlaris")
        st.bar_chart(df_top.set_index("product_name"))
    else:
        st.info("Belum ada data penjualan produk.")

    st.markdown("---")

    # ============================
    # 3. PENJUALAN PER BULAN
    # ============================
    result_sales = sales_per_month()

    if result_sales:
        df_sales = pd.DataFrame(result_sales, columns=["month", "total_sales"])
        df_sales["month"] = pd.to_datetime(df_sales["month"])

        # Format rupiah untuk tampilan tabel
        df_sales["total_sales_rp"] = df_sales["total_sales"].apply(
            lambda x: f"Rp {x:,.0f}".replace(",", ".")
        )

        st.subheader("📅 Total Penjualan per Bulan (Grafik)")
        st.line_chart(df_sales.set_index("month")["total_sales_rp"])

    else:
        st.info("Belum ada data penjualan bulanan.")
