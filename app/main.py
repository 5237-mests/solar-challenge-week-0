import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import kruskal # For statistical testing

# --- Page Configuration ---
st.set_page_config(
    page_title="Solar Potential Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global Data Paths and Metrics ---
DATA_DIR = os.path.join("..", "data") # Assumes 'data' folder is one level up
COUNTRIES = ["Benin", "SierraLeone", "Togo"]
SOLAR_METRICS = ["GHI", "DNI", "DHI"]

# --- Data Loading Functions ---
@st.cache_data
def load_single_country_data(country_name):
    """Loads clean CSV data for a given country."""
    file_path = os.path.join(DATA_DIR, f"{country_name.lower()}_clean.csv")
    try:
        df = pd.read_csv(file_path)
        st.sidebar.success(f"Successfully loaded {country_name} data!")
        return df
    except FileNotFoundError:
        st.error(f"Error: Data file not found for {country_name} at {file_path}. "
                 "Please ensure the 'data' folder is one level up and contains the CSVs.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred loading {country_name} data: {e}")
        return pd.DataFrame()

@st.cache_data
def load_all_country_data():
    """
    Loads clean CSV data for all specified countries and combines them
    into a single DataFrame with a 'Country' column.
    """
    all_dfs = []
    load_errors = []

    for country in COUNTRIES:
        print(f"Loading data for {country}...")
        file_path = os.path.join(DATA_DIR, f"{country.lower()}_clean.csv")
        try:
            df = pd.read_csv(file_path)
            df['Country'] = country # Add a country column
            all_dfs.append(df)
        except FileNotFoundError:
            load_errors.append(f"Data file not found for {country} at {file_path}.")
        except Exception as e:
            load_errors.append(f"An error occurred loading {country} data: {e}")

    if load_errors:
        for error_msg in load_errors:
            st.sidebar.error(error_msg) # Show errors in sidebar
        st.error("Some data files could not be loaded. Please check data directory and file names.")
        return pd.DataFrame()

    if not all_dfs:
        st.error("No dataframes were loaded successfully. Please ensure your data directory is correct.")
        return pd.DataFrame()

    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Check for presence of solar metrics
    missing_metrics = [metric for metric in SOLAR_METRICS if metric not in combined_df.columns]
    if missing_metrics:
        st.error(f"Critical solar potential columns missing from your data: {', '.join(missing_metrics)}. "
                 "Please ensure your CSVs contain 'GHI', 'DNI', and 'DHI' columns.")
        return pd.DataFrame() # Return empty if essential columns are missing

    st.sidebar.success("All country data loaded successfully!")
    return combined_df

# --- Visualization Functions (Modularized) ---

def display_single_country_insights(df, selected_country):
    """Displays visualizations for a single selected country."""
    st.header(f"Insights for {selected_country}")

    # Identify numeric and categorical columns for flexible plotting
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Single Country Viz Options")

    # Dynamic filter for a numeric column (if available)
    df_filtered = df
    if numeric_cols:
        default_numeric_col = numeric_cols[0] if numeric_cols else None
        if default_numeric_col and not df[default_numeric_col].isnull().all():
            min_val = df[default_numeric_col].min()
            max_val = df[default_numeric_col].max()
            value_range = st.sidebar.slider(
                f"Filter by {default_numeric_col}",
                float(min_val),
                float(max_val),
                (float(min_val), float(max_val))
            )
            df_filtered = df[(df[default_numeric_col] >= value_range[0]) & (df[default_numeric_col] <= value_range[1])]
        else:
            st.sidebar.info("No suitable numeric column for filtering example.")
    else:
        st.sidebar.info("No numeric columns found for filtering.")

    # Select box for X and Y axes for scatter plot
    st.sidebar.markdown("### Chart Axes Selection")
    x_axis_options = numeric_cols + categorical_cols
    y_axis_options = numeric_cols

    if not x_axis_options:
        st.warning("No columns available for X-axis selection.")
        return
    if not y_axis_options:
        st.warning("No numeric columns available for Y-axis selection.")
        return

    x_axis_col = st.sidebar.selectbox(
        "Select X-axis",
        x_axis_options,
        index=0 if x_axis_options else 0 # Ensure default if list not empty
    )
    y_axis_col = st.sidebar.selectbox(
        "Select Y-axis",
        y_axis_options,
        index=0 if y_axis_options else 0 # Ensure default if list not empty
    )

    visualization_type = st.sidebar.selectbox(
        "Choose Visualization Type",
        ("Data Table", "Histogram (Numeric)", "Bar Chart (Categorical)", "Scatter Plot")
    )

    st.markdown(f"### Selected Visualization: {visualization_type}")

    if visualization_type == "Data Table":
        st.dataframe(df_filtered, use_container_width=True)
    elif visualization_type == "Histogram (Numeric)":
        if x_axis_col in numeric_cols:
            fig = px.histogram(df_filtered, x=x_axis_col, title=f'Distribution of {x_axis_col}')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Please select a numeric column for the Histogram. '{x_axis_col}' is not numeric.")
    elif visualization_type == "Bar Chart (Categorical)":
        if x_axis_col in categorical_cols:
            category_counts = df_filtered[x_axis_col].value_counts().reset_index()
            category_counts.columns = [x_axis_col, 'Count']
            fig = px.bar(
                category_counts, x=x_axis_col, y='Count',
                title=f'Count of Records by {x_axis_col}', template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        elif x_axis_col in numeric_cols:
            st.warning(f"'{x_axis_col}' is numeric. Consider a histogram instead.")
        else:
            st.warning("Please select a categorical column for the Bar Chart.")
    elif visualization_type == "Scatter Plot":
        if x_axis_col in df_filtered.columns and y_axis_col in df_filtered.columns:
            color_col = categorical_cols[0] if categorical_cols else None
            fig = px.scatter(
                df_filtered, x=x_axis_col, y=y_axis_col,
                color=color_col, title=f'{y_axis_col} vs {x_axis_col}',
                template="plotly_white", hover_data=df_filtered.columns
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please select valid X and Y axis columns for the Scatter Plot.")

    st.markdown("---")
    st.subheader("Key Statistics")
    if not df_filtered.empty and numeric_cols:
        st.dataframe(df_filtered[numeric_cols].describe())
    else:
        st.info("No numeric data available to display key statistics for the filtered dataset.")


def display_cross_country_comparison(combined_df):
    """Displays comparative visualizations and statistics across all countries."""
    st.header("Cross-Country Solar Potential Comparison")
    st.markdown("Explore the distribution and key statistics of solar potential metrics across Benin, Sierra Leone, and Togo.")

    selected_metrics_for_comp = st.sidebar.multiselect(
        "Select Metrics for Comparison",
        SOLAR_METRICS,
        default=SOLAR_METRICS
    )
    selected_countries_for_comp = st.sidebar.multiselect(
        "Select Countries for Comparison",
        COUNTRIES,
        default=COUNTRIES
    )

    filtered_comp_df = combined_df[combined_df["Country"].isin(selected_countries_for_comp)]

    if filtered_comp_df.empty:
        st.warning("No data to display for the selected countries.")
        return

    # Boxplots for each selected metric
    st.subheader("1. Metric Distribution Boxplots")
    for metric in selected_metrics_for_comp:
        if metric in filtered_comp_df.columns:
            st.markdown(f"**{metric} Distribution by Country**")
            fig = px.box(
                filtered_comp_df,
                x='Country',
                y=metric,
                color='Country',
                title=f'Box Plot of {metric} across Selected Countries',
                labels={metric: f'{metric} (Units)'}, # Placeholder for units
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"'{metric}' column not found in data.")

    st.markdown("---")

    # Summary Table
    st.subheader("2. Summary Statistics Table")
    if selected_metrics_for_comp:
        summary_stats_df = filtered_comp_df.groupby('Country')[selected_metrics_for_comp].agg(
            Mean=('mean'),
            Median=('median'),
            Std_Dev=('std')
        ).unstack().reset_index()

        summary_stats_df.columns = ['Metric', 'Statistic', 'Value']
        summary_stats_pivot = summary_stats_df.pivot_table(index='Metric', columns='Statistic', values='Value')
        summary_stats_pivot = summary_stats_pivot[['Mean', 'Median', 'Std_Dev']] # Ensure order

        st.dataframe(summary_stats_pivot.round(2), use_container_width=True)
    else:
        st.info("Select at least one metric to display summary statistics.")

    st.markdown("---")

    # Kruskal-Wallis Test
    st.subheader("3. Kruskal–Wallis H-test for GHI")
    st.info("The Kruskal–Wallis H-test is a non-parametric method for testing whether samples originate from the same distribution. It is used here to compare GHI across selected countries.")
    if "GHI" in selected_metrics_for_comp and len(selected_countries_for_comp) > 1:
        valid_groups = []
        for country in selected_countries_for_comp:
            country_data = filtered_comp_df[filtered_comp_df["Country"] == country]["GHI"].dropna()
            if not country_data.empty:
                valid_groups.append(country_data)
            else:
                st.warning(f"No GHI data for {country} or all values are NaN. Skipping {country} in Kruskal-Wallis test.")

        if len(valid_groups) >= 2: # Kruskal-Wallis requires at least 2 groups
            result = kruskal(*valid_groups)
            st.write(f"**Kruskal–Wallis p-value (for GHI)**: `{result.pvalue:.4f}`")
            if result.pvalue < 0.05:
                st.success("Result: There is a statistically significant difference in GHI between the selected countries.")
            else:
                st.info("Result: No statistically significant difference in GHI found between the selected countries.")
        else:
            st.warning("Not enough valid groups (countries with GHI data) to perform Kruskal–Wallis test.")
    else:
        st.info("Select 'GHI' and at least two countries to run the Kruskal–Wallis test.")

    st.markdown("---")

    # Average GHI Bar Chart
    st.subheader("4. Average GHI by Country")
    if "GHI" in selected_metrics_for_comp:
        avg_ghi = filtered_comp_df.groupby("Country")["GHI"].mean().sort_values(ascending=False).reset_index()
        fig_avg_ghi = px.bar(
            avg_ghi, x="Country", y="GHI",
            title="Average GHI by Country",
            template="plotly_white", color="Country"
        )
        st.plotly_chart(fig_avg_ghi, use_container_width=True)
    else:
        st.info("Select 'GHI' to display the Average GHI bar chart.")


# --- Main Application Logic ---
def main():
    st.sidebar.image("https://www.streamlit.io/logo.svg", width=150) # Example logo
    st.sidebar.title("Navigation")
    analysis_mode = st.sidebar.radio(
        "Choose Analysis Mode",
        ("Individual Country Analysis", "Cross-Country Comparison")
    )

    if analysis_mode == "Individual Country Analysis":
        st.markdown("---")
        st.header("🌍 Individual Country Data Explorer")
        st.markdown("Select a single country to delve into its specific data distributions and patterns.")

        selected_country = st.sidebar.selectbox(
            "Select a Country",
            COUNTRIES
        )
        df_single = load_single_country_data(selected_country)

        if not df_single.empty:
            display_single_country_insights(df_single, selected_country)
        else:
            st.warning("Please resolve data loading issues to view individual country insights.")

    elif analysis_mode == "Cross-Country Comparison":
        st.markdown("---")
        st.header("📈 Cross-Country Solar Potential Overview")
        st.markdown("Compare GHI, DNI, and DHI across selected West African countries for a holistic view of solar potential.")

        combined_df = load_all_country_data()

        if not combined_df.empty:
            display_cross_country_comparison(combined_df)
        else:
            st.warning("Please resolve data loading issues to perform cross-country comparisons.")

    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit for data insights.")

if __name__ == "__main__":
    main()