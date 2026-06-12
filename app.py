import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import load_data

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Analytics Dashboard (PRO VERSION)")

# ---------------- LOAD DATA ----------------
df = load_data()
df.columns = df.columns.str.strip()

# ---------------- FILTER ----------------
st.sidebar.header("Filters")

region = st.sidebar.selectbox("Select Region", ["All"] + df["Region"].unique().tolist())

if region == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Region"] == region]

# ---------------- KPI SECTION ----------------
st.markdown("## 📌 Key Performance Indicators")

total_sales = filtered_df["Sales"].sum()
total_orders = len(filtered_df)

top_product_data = filtered_df.groupby("Product")["Sales"].sum().reset_index()
top_product_data = top_product_data.sort_values("Sales", ascending=False)

if len(top_product_data) > 0:
    top_product = top_product_data.iloc[0]["Product"]
else:
    top_product = "N/A"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", f"₹{total_sales}")

with col2:
    st.metric("Total Orders", total_orders)

with col3:
    st.metric("Top Product", top_product)

st.divider()

# ---------------- TABLE ----------------
st.markdown("## 📋 Sales Data Table")
st.dataframe(filtered_df)

st.divider()

# ---------------- PRODUCT CHART ----------------
st.markdown("## 📊 Product Wise Sales")

product_sales = filtered_df.groupby("Product")["Sales"].sum().reset_index()

fig, ax = plt.subplots()
ax.bar(product_sales["Product"], product_sales["Sales"])
ax.set_xlabel("Product")
ax.set_ylabel("Sales")

st.pyplot(fig)

st.divider()

# ---------------- REGION CHART ----------------
st.markdown("## 🌍 Region Wise Sales")

region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig2, ax2 = plt.subplots()
ax2.pie(region_sales["Sales"], labels=region_sales["Region"], autopct="%1.1f%%")

st.pyplot(fig2)

st.divider()

# ---------------- DOWNLOAD ----------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    "📥 Download Report",
    data=csv,
    file_name="sales_report.csv",
    mime="text/csv"
)