import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
df = pd.read_csv("simple_customer_data.csv")

st.sidebar.header("🎛️ Data Filters")
selected_cities = st.sidebar.multiselect("City", df["City"].unique(), default=df["City"].unique())
selected_genders = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())
selected_products = st.sidebar.multiselect("Product Category", df["Product_Category"].unique(), default=df["Product_Category"].unique())

filtered_df = df[
    (df["City"].isin(selected_cities)) &
    (df["Gender"].isin(selected_genders)) &
    (df["Product_Category"].isin(selected_products))
]

st.title("📊 Advanced Interactive Customer Dashboard")


st.subheader("💡 Product Sales Scorecards")
score_cols = st.columns(len(df["Product_Category"].unique()))
for i, product in enumerate(df["Product_Category"].unique()):
    total_sales = filtered_df[filtered_df["Product_Category"] == product]["Purchase_Amount"].sum()
    score_cols[i].metric(label=product, value=f"{total_sales:,.2f}")

st.markdown("---")


st.subheader("🔍 Core Visualizations")

st.markdown("**Distribution of Purchase Amount**")
fig1, ax1 = plt.subplots()
sns.histplot(filtered_df['Purchase_Amount'], bins=20, kde=True, ax=ax1, color='skyblue')
ax1.set_xlabel("Purchase Amount")
ax1.set_ylabel("Frequency")
st.pyplot(fig1)

st.markdown("**Purchase Count by Product Category and Gender**")
product_by_gender = filtered_df.groupby(["Gender", "Product_Category"]).size().reset_index(name="Purchase_Count")
fig2, ax2 = plt.subplots()
sns.barplot(data=product_by_gender, x="Product_Category", y="Purchase_Count", hue="Gender", ax=ax2, palette="Set2")
st.pyplot(fig2)

st.markdown("**Top-Selling Product Category Per Gender**")
top_product_gender = product_by_gender.sort_values("Purchase_Count", ascending=False).groupby("Gender").first().reset_index()
fig3, ax3 = plt.subplots()
sns.barplot(data=top_product_gender, x="Gender", y="Purchase_Count", hue="Product_Category", dodge=False, ax=ax3, palette="pastel")
st.pyplot(fig3)

st.markdown("**Total Sales by Product Category**")
product_sales = filtered_df.groupby("Product_Category")["Purchase_Amount"].sum().reset_index().sort_values("Purchase_Amount", ascending=False)
fig4, ax4 = plt.subplots()
sns.barplot(data=product_sales, x="Purchase_Amount", y="Product_Category", palette="viridis", ax=ax4)
st.pyplot(fig4)

st.markdown("**Top Purchasing Age By Gender**")
age_gender_distribution = filtered_df.groupby(["Gender", "Age"]).size().reset_index(name="Purchase_Count")
top_ages_by_gender = age_gender_distribution.sort_values("Purchase_Count", ascending=False).groupby("Gender").first().reset_index()
fig5, ax5 = plt.subplots()
sns.barplot(data=top_ages_by_gender, x="Gender", y="Purchase_Count", hue="Age", dodge=False, ax=ax5, palette="cool")
st.pyplot(fig5)

st.markdown("**Top-Selling Product Category Per City**")
city_product_counts = filtered_df.groupby(["City", "Product_Category"]).size().reset_index(name="Purchase_Count")
top_product_by_city = city_product_counts.sort_values("Purchase_Count", ascending=False).groupby("City").first().reset_index()
fig6, ax6 = plt.subplots()
sns.barplot(data=top_product_by_city, x="City", y="Purchase_Count", hue="Product_Category", dodge=False, ax=ax6)
st.pyplot(fig6)

st.markdown("**Least-Selling Product Category Per City**")
least_product_by_city = city_product_counts.sort_values("Purchase_Count").groupby("City").first().reset_index()
fig7, ax7 = plt.subplots()
sns.barplot(data=least_product_by_city, x="City", y="Purchase_Count", hue="Product_Category", dodge=False, ax=ax7, palette="Set1")
st.pyplot(fig7)


st.markdown("---")
st.subheader("📈 Advanced Correlation Heatmap")

fig8, ax8 = plt.subplots()
sns.heatmap(filtered_df.select_dtypes(include='number').corr(), annot=True, cmap='Blues', ax=ax8)
st.pyplot(fig8)

st.markdown("---")
st.caption("🚀 Built with Streamlit for portfolio & CV presentation.")
