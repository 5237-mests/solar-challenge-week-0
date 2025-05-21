import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kruskal

# ---- Page Config ----
st.set_page_config(page_title="Solar Potential Comparison", layout="wide")

# ---- Title ----
st.title("☀️ Cross-Country Solar Potential Dashboard")
st.markdown("Compare **GHI**, **DNI**, and **DHI** metrics across Benin, Sierra Leone, and Togo.")

# ---- Load Data ----
@st.cache_data
def load_data():
    benin = pd.read_csv("../data/benin_clean.csv")
    sierraleone = pd.read_csv("../data/sierraleone_clean.csv")
    togo = pd.read_csv("../data/togo_clean.csv")

    benin["Country"] = "Benin"
    sierraleone["Country"] = "Sierra Leone"
    togo["Country"] = "Togo"

    return pd.concat([benin, sierraleone, togo], ignore_index=True)

df = load_data()

# ---- Sidebar Filters ----
st.sidebar.header("🔧 Filters")
metric = st.sidebar.selectbox("Select metric", ["GHI", "DNI", "DHI"])
selected_countries = st.sidebar.multiselect(
    "Select countries", ["Benin", "Sierra Leone", "Togo"], default=["Benin", "Sierra Leone", "Togo"]
)

# ---- Filter Data ----
filtered_df = df[df["Country"].isin(selected_countries)]

# ---- Boxplot ----
st.subheader(f"📦 Boxplot of {metric}")
fig, ax = plt.subplots()
# Set the figure size
fig.set_size_inches(10, 6)
sns.boxplot(x="Country", y=metric, data=filtered_df, palette="Set2", hue="Country", ax=ax)
ax.set_title(f"{metric} Distribution by Country")
st.pyplot(fig)

# ---- Summary Table ----
st.subheader("📊 Summary Statistics")
summary = (
    filtered_df.groupby("Country")[["GHI", "DNI", "DHI"]]
    .agg(["mean", "median", "std"])
    .round(2)
)
st.dataframe(summary)

# ---- ANOVA (Kruskal-Wallis) ----
st.subheader("📈 Kruskal–Wallis Test (GHI only)")

if all(c in filtered_df["Country"].unique() for c in ["Benin", "Sierra Leone", "Togo"]):
    groups = [
        filtered_df[filtered_df["Country"] == c]["GHI"]
        for c in ["Benin", "Sierra Leone", "Togo"]
    ]
    result = kruskal(*groups)
    st.write(f"**Kruskal–Wallis p-value**: `{result.pvalue:.4f}`")
    if result.pvalue < 0.05:
        st.success("There is a statistically significant difference in GHI between the countries.")
    else:
        st.info("No statistically significant difference in GHI.")
else:
    st.warning("Kruskal–Wallis test requires all three countries.")

# ---- Average GHI Bar Chart ----
st.subheader("🏅 Average GHI by Country")
avg_ghi = filtered_df.groupby("Country")["GHI"].mean().sort_values(ascending=False).reset_index()

fig2, ax2 = plt.subplots()
# Set the figure size
fig2.set_size_inches(10, 6)
# Create a bar plot
sns.barplot(data=avg_ghi, x="Country", y="GHI", palette="viridis", hue='Country', legend=False, ax=ax2)
ax2.set_title("Average GHI")
st.pyplot(fig2)

# ---- Footer ----
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit.")