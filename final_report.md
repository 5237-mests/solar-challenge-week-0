# Week 0 Final Report – Solar Potential Analysis

![Solar Dashboard Banner](https://github.com/5237-mests/solar-challenge-week-0/blob/main/dashboard_screenshots/dashboard4.PNG?raw=true)

### 👤 Name: Mesfin Mulugeta Wetere

### 🔹 Date: May 21, 2025

### 🔹 GitHub Repository: [5237-mests/solar-challenge-week-0](https://github.com/5237-mests/solar-challenge-week-0)

### 📅 Week: 0

### 📍 Project: Solar Energy Potential Comparison (Benin, Sierra Leone, Togo)

---

## ✅ Objectives

- Compare solar energy metrics (**GHI**, **DNI**, **DHI**) across selected West African countries.
- Clean and merge country-specific datasets.
- Perform descriptive analysis and statistical testing (Kruskal–Wallis).
- Visualize insights through static and interactive dashboards using Matplotlib, Seaborn, and Streamlit.

---

## 📊 Data Sources

- Cleaned datasets:
  - `benin_clean.csv`
  - `sierraleone_clean.csv`
  - `togo_clean.csv`
- Columns: `GHI`, `DNI`, `DHI`, `Temperature`, `Wind Speed`, etc.

---

## 🧼 Data Cleaning & Preprocessing

- Handled missing values using `.dropna()` and `.fillna()`.
- Removed column 'comments' wich have 100% missing values.
- Converted timestamps (if any) and normalized columns.
- Removed outliers.
- Added a `Country` column to each dataset before merging.

---

## 📈 Key Analyses & Visualizations

- **Boxplots** for GHI, DNI, DHI by country.
- **Summary statistics** table (mean, median, std).
- **Kruskal–Wallis test** to assess statistical significance in GHI.
- **Bar chart** showing average GHI per country.

---

## 📊 Insights

- Benin and Togo had higher average GHI values compared to Sierra Leone.
- The Kruskal–Wallis test showed **[significant]** difference in GHI across countries (p-value = `0.0000`).
- GHI variability is visibly higher in **[Benin]** based on boxplot distribution.

---

## 💻 Streamlit Dashboard

- Built an **interactive app** to:
  - Select metrics and countries.
  - View updated boxplots and summaries.
  - Run real-time Kruskal–Wallis test.
- Used `@st.cache_data` to optimize data loading.
- Set figure size to `(7, 3)` for cleaner visuals.

---

## 🔧 Tools Used

- **Pandas** for data handling
- **matplotlib** and **seaborn** for visualization
- **Seaborn & Matplotlib** for visualization
- **Scipy** for statistical analysis
- **Streamlit** for dashboard interface

---

## 🚀 Challenges Faced

- learning curve for data analysis.
- learning curve for dashboard development with Streamlit.
- Balancing interactivity and performance in Streamlit.
- Ensuring consistent column naming across datasets.
- deployment issues with Streamlit.
- Warning when using `palette` in `sns.barplot()` without `hue`.
- Ensuring consistent column naming across datasets.
- Time constraint for Streamlit deployment and testing.

---

## ✅ Final Thoughts

This project gave me hands-on experience with:

- Exploratory data analysis (EDA)
- Data cleaning and preprocessing
- Statistical analysis
- Data visualization
- Dashboard development
- Familiarity with Python libraries like Pandas, Matplotlib, Seaborn.
- Familiarity with Streamlit for interactive dashboards.
- Real-world solar energy datasets
- Dashboard creation using Streamlit

It helped solidify my skills in Python, data storytelling, and presenting insights in a clear and engaging way.
