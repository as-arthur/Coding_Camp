import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_revenue_by_year_df(df):
    revenue_by_year_df = (
    all_orders_df
    .groupby(all_orders_df['order_purchase_timestamp'].dt.year)['price']
    .sum()
    .reset_index()
    )

    return revenue_by_year_df

def create_category_revenue_df (df):
    category_revenue_df = (
       order_product_2018_translate_df
    .groupby('product_category_name_english')['price']
    .sum()
    .sort_values(ascending=False)
    .reset_index() 
    )

    return category_revenue_df

def create_rfm_data_df (df):
    rfm_data_df= pd.merge(
    left=orders_df,
    right=order_payments_df,
    how="left",
    left_on="order_id",
    right_on="order_id"
    )
    rfm_data_df = pd.merge(
    left=rfm_data_df,
    right=costumers_df,
    how="left",
    left_on="customer_id",
    right_on="customer_id"
    )
    rfm_data_df.columns = ["customer_unique_id", "recency", "frequency", "monetary"]

    tanggal = rfm_data_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

    rfm_data_df = rfm_data_df.groupby(by="customer_unique_id").agg({
    "order_purchase_timestamp" : lambda x: (tanggal - x.max()).days,
    "order_id" : "nunique",
    "payment_value" : "sum"
    })

    return rfm_data_df

# Load cleaned data
combined_df = pd.read_csv("D:\Semester 6\Coding Camp 2025\latihan\Coding_Camp\dashboard\combined_df.csv")

datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "shipping_limit_date"]
combined_df.sort_values(by="order_purchase_timestamp", inplace=True)
combined_df.reset_index(inplace=True)

for column in datetime_columns:
    combined_df[column] = pd.to_datetime(combined_df[column])

# Filter data
min_date = combined_df["order_purchase_timestamp"].min()
max_date = combined_df["order_purchase_timestamp"].max()

with st.sidebar:
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )