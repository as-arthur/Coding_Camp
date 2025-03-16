import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from babel.numbers import format_currency

sns.set(style='dark')

def create_revenue_by_year_df(df):
    revenue_by_year_df = (
        df.groupby(df["order_purchase_timestamp"].dt.year)["price"]
        .sum()
        .reset_index()
    )

    return revenue_by_year_df

def create_category_revenue_df(df):
    df_filtered = df[df["order_purchase_timestamp"].dt.year == 2018]  # Filter tahun 2018
    category_revenue_df = (
        df_filtered.groupby("product_category_name_english")["price"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return category_revenue_df

def create_rfm_data_df(df):
    tanggal = df["order_purchase_timestamp"].max()  # Definisikan tanggal lebih dulu
    
    rfm_data_df = df.groupby(by="customer_unique_id").agg({
        "order_purchase_timestamp": lambda x: (tanggal - x.max()).days,  # Recency
        "order_id": "nunique",  # Frequency
        "payment_value": "sum"  # Monetary
    }).reset_index()
    
    rfm_data_df.rename(columns={"order_purchase_timestamp": "recency"}, inplace=True)
    rfm_data_df.rename(columns={"order_id": "frequency"}, inplace=True)
    rfm_data_df.rename(columns={"payment_value": "monetary"}, inplace=True)

    # Pembuatan skor RFM
    rfm_data_df["R_score"] = pd.qcut(rfm_data_df["recency"], q=5, labels=[5, 4, 3, 2, 1])
    rfm_data_df["F_score"] = pd.qcut(rfm_data_df["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5])
    rfm_data_df["M_score"] = pd.qcut(rfm_data_df["monetary"], q=5, labels=[1, 2, 3, 4, 5])

    rfm_data_df["RFM_score"] = rfm_data_df["R_score"].astype(int) + rfm_data_df["F_score"].astype(int) + rfm_data_df["M_score"].astype(int)
    
    return rfm_data_df

def create_seller_map_df(df, seller_df, geolocation_df):
    seller_map_df = pd.merge(
        left=seller_df,
        right=geolocation_df,
        how="left",
        left_on="seller_zip_code_prefix",
        right_on="geolocation_zip_code_prefix"
    )

    seller_map_df = seller_map_df.groupby(["geolocation_lat", "geolocation_lng"]).agg({
        "seller_id": "nunique",
    }).sort_values(by="seller_id", ascending=False).reset_index()

    return seller_map_df

def created_product_orders_df(df):
    product_orders_df = df[["product_id", "price", "product_weight_g", "freight_value"]].copy()

    product_orders_df['price_category'] = pd.cut(
        product_orders_df['price'],
        bins=[0, 40, 75, 135, float('inf')],
        labels=['low', 'medium', 'high', 'very_high']
    )
    product_orders_df['weight_category'] = pd.cut(
        product_orders_df['product_weight_g'],
        bins=[0, 300, 700, 1800, float('inf')],
        labels=['light', 'medium', 'heavy', 'very_heavy']
    )

    return product_orders_df

# Load cleaned data
combined_df = pd.read_csv("D:\Semester 6\Coding Camp 2025\latihan\Coding_Camp\dashboard\combined_df.csv")

datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "shipping_limit_date"]
combined_df.sort_values(by="order_purchase_timestamp", inplace=True)
combined_df.reset_index(drop=True, inplace=True)

for column in datetime_columns:
    combined_df[column] = pd.to_datetime(combined_df[column], errors='coerce')

# Load data
seller_df = pd.read_csv("D:/Semester 6/Coding Camp 2025/latihan/Coding_Camp/data/sellers_dataset.csv")
geolocation_df = pd.read_csv("D:\Semester 6\Coding Camp 2025\latihan\Coding_Camp\data\geolocation_dataset.csv")

# Filter data
min_date = combined_df["order_purchase_timestamp"].min()
max_date = combined_df["order_purchase_timestamp"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

main_df = combined_df[
    (combined_df["order_purchase_timestamp"] >= start_date) & 
    (combined_df["order_purchase_timestamp"] <= end_date)
]

# Menyiapkan berbagai dataframe
revenue_by_year_df = create_revenue_by_year_df(main_df)
category_revenue_df = create_category_revenue_df(main_df)
rfm_data_df = create_rfm_data_df(main_df)
seller_map_df = create_seller_map_df(main_df, seller_df, geolocation_df)
product_orders_df = created_product_orders_df(main_df)

# Revenue Performance
st.subheader("Revenue Performance from 2016 to 2018")

# Buat dataframe revenue berdasarkan tahun
revenue_by_year_df = (
    combined_df.groupby(combined_df["order_purchase_timestamp"].dt.year)["price"]
    .sum()
    .reset_index()
)

# Plot Revenue Performance
fig, ax = plt.subplots(figsize=(8, 4))  # Sesuaikan ukuran fig agar tidak terlalu besar
sns.barplot(
    x="order_purchase_timestamp",
    y="price",
    data=revenue_by_year_df,
    palette="Blues"
)

ax.set_ylabel("Total Revenue", fontsize=12)
ax.set_xlabel("Year", fontsize=12)
ax.set_title("Revenue Performance (2016-2018)", fontsize=14)

# Tambahkan label nilai di atas batang
for i, value in enumerate(revenue_by_year_df["price"]):
    ax.text(i, value + 50000, format_currency(value, "ARS", locale="es_AR"), ha="center", fontsize=10, fontweight="bold")

st.pyplot(fig)

# Category Performances
st.subheader("Top 5 Best Performing Categories by Revenue")

# Ambil 5 kategori dengan revenue tertinggi
top_5_categories = category_revenue_df.head(5)

# Plot Best Categories
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="price", 
    x="product_category_name_english", 
    data=top_5_categories, 
    palette=["#90CAF9"] * 5,  
    ax=ax
)

ax.set_ylabel("Total Revenue", fontsize=12)
ax.set_xlabel("Product Category", fontsize=12)
ax.set_title("Top 5 Best Performing Categories", fontsize=14)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")

# Tambahkan label nilai di atas batang
for i, value in enumerate(top_5_categories["price"]):
    ax.text(i, value + 5000, format_currency(value, "ARS", locale="es_AR"), ha="center", fontsize=10, fontweight="bold")

st.pyplot(fig)

# Worst Performing Categories
st.subheader("Top 5 Worst Performing Categories by Revenue")

# Ambil 5 kategori dengan revenue terendah
bottom_5_categories = category_revenue_df.tail(5)

# Plot Worst Categories
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="price", 
    x="product_category_name_english", 
    data=bottom_5_categories, 
    palette=["#E53935"] * 5,  
    ax=ax
)

ax.set_ylabel("Total Revenue", fontsize=12)
ax.set_xlabel("Product Category", fontsize=12)
ax.set_title("Top 5 Worst Performing Categories", fontsize=14)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")

# Tambahkan label nilai di atas batang
for i, value in enumerate(bottom_5_categories["price"]):
    ax.text(i, value + (value * 0.005), format_currency(value, "ARS", locale="es_AR"), ha="center", fontsize=10, fontweight="bold")

st.pyplot(fig)

# Best Customer Based on RFM Parameters
st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_data_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_data_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(rfm_data_df.monetary.mean(), "ARS", locale='es_AR') 
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(
    y="recency", 
    x="customer_unique_id", 
    data=rfm_data_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35, rotation=90)

sns.barplot(
    y="frequency", 
    x="customer_unique_id",
      data=rfm_data_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35, rotation=90)

sns.barplot(
    y="monetary", 
    x="customer_unique_id", 
    data=rfm_data_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35, rotation=90)

st.pyplot(fig)

# Visualisasi Distribusi Jumlah Customer Berdasarkan RFM Score
st.subheader("Distribution of Customers by RFM Score")

# Hitung jumlah customer per RFM score
rfm_score_counts = rfm_data_df["RFM_score"].value_counts().reset_index()
rfm_score_counts.columns = ["RFM_score", "customer_count"]
rfm_score_counts = rfm_score_counts.sort_values(by="RFM_score", ascending=False)


fig, ax = plt.subplots(figsize=(15, 8))

sns.barplot(
    y="customer_count", 
    x="RFM_score", 
    data=rfm_score_counts, 
    palette=colors, 
    ax=ax
)

ax.set_ylabel("Number of Customers", fontsize=15)
ax.set_xlabel("RFM Score", fontsize=15)
ax.set_title("Customer Distribution by RFM Score", fontsize=20)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

st.pyplot(fig)


# The Distribution of Sellers
st.subheader("Most Dense Seller in Argentina")

# Drop NaN values from the dataset
product_orders_df = product_orders_df.dropna()

# Ensure categorical columns are strings instead of category type
product_orders_df["price_category"] = product_orders_df["price_category"].astype(str)
product_orders_df["weight_category"] = product_orders_df["weight_category"].astype(str)

# Create group_data from product_orders_df
group_data = product_orders_df.groupby(["price_category", "weight_category"], as_index=False).agg({
    "freight_value": "sum"
})


group_data = group_data.sort_values(by="freight_value", ascending=True)

# Plot 1: Total Freight Value by Price Category
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="price_category",
    y="freight_value",
    data=group_data.groupby("price_category", as_index=False).sum().sort_values(by="freight_value", ascending=True),
    palette="Blues",
    ax=ax1
)
ax1.set_title("Total Shipping Cost by Price Category", fontsize=14)
ax1.set_xlabel("Product Price Category", fontsize=12)
ax1.set_ylabel("Total Shipping Cost (Freight Value)", fontsize=12)
ax1.tick_params(axis='x', rotation=45)  

st.pyplot(fig1)

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="weight_category",
    y="freight_value",
    data=group_data.groupby("weight_category", as_index=False).sum().sort_values(by="freight_value", ascending=True),
    palette="Oranges",
    ax=ax2
)
ax2.set_title("Total Shipping Cost by Weight Category", fontsize=14)
ax2.set_xlabel("Product Weight Category", fontsize=12)
ax2.set_ylabel("Total Shipping Cost (Freight Value)", fontsize=12)
ax2.tick_params(axis='x', rotation=45) 

st.pyplot(fig2)