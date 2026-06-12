import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import load_data

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Analytics Dashboard (PRO VERSION)")

# ---------------- LOAD DATA ----------------
df = load_data()

# ---------------- SAVE CSV (optional local file) ----------------
df.to_csv("sales_data.csv", index=False)

# ---------------- CLEAN COLUMN NAMES ----------------
df.columns = df.columns.str.strip()

# ---------------- FILTER ----------------
st.sidebar.header("Filters")

region_list = ["All"] + list(df["Region"].unique())
region = st.sidebar.selectbox("Select Region", region_list)

if region == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Region"] == region]

# ---------------- KPI SECTION ----------------
st.markdown("## 📌 Key Performance Indicators")

total_sales = filtered_df["Sales"].sum()
total_orders = len(filtered_df)

top_product_df = filtered_df.groupby("Product")["Sales"].sum().reset_index()

if not top_product_df.empty:
    top_product = top_product_df.sort_values("Sales", ascending=False).iloc[0]["Product"]
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
st.subheader("Sales Data Table")
st.dataframe(filtered_df)

st.divider()

# ---------------- PRODUCT CHART ----------------
st.subheader("Product Wise Sales")

product_sales = filtered_df.groupby("Product")["Sales"].sum().reset_index()

fig, ax = plt.subplots()
ax.bar(product_sales["Product"], product_sales["Sales"])
ax.set_xlabel("Product")
ax.set_ylabel("Sales")
st.pyplot(fig)

st.divider()

# ---------------- REGION CHART ----------------
st.subheader("Region Wise Sales")

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