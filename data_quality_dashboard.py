import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Define functions for data quality checks
def perform_completeness_check(df):
    missing_values = df.isnull().sum().sum()
    total_values = df.size
    completeness = ((total_values - missing_values) / total_values) * 100
    return completeness, missing_values

def perform_uniqueness_check(df, column):
    duplicate_rows = df.duplicated(subset=[column]).sum()
    return duplicate_rows

def perform_validity_check(df, column, valid_values):
    valid_entries = df[column].isin(valid_values).sum()
    validity = (valid_entries / len(df)) * 100
    return validity

# Set up the Streamlit app
st.set_page_config(page_title="Data Quality Dashboard", layout="wide")

# Title and Description
st.title("Data Quality Dashboard")
st.markdown("Analyze data quality using metrics such as **Completeness**, **Uniqueness**, and **Validity**.")

# Upload Dataset Section
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Display data preview
    st.subheader("Uploaded Data")
    st.dataframe(df.head())

    # Data Overview
    st.sidebar.header("Select Columns for Quality Checks")
    selected_column = st.sidebar.selectbox("Select a column for uniqueness check", df.columns)

    # Completeness Check
    completeness, missing_values = perform_completeness_check(df)
    st.sidebar.header("Completeness Check")
    st.sidebar.write(f"Completeness: {completeness:.2f}%")
    st.sidebar.write(f"Missing Values: {missing_values}")

    # Uniqueness Check
    duplicate_rows = perform_uniqueness_check(df, selected_column)
    st.sidebar.header("Uniqueness Check")
    st.sidebar.write(f"Duplicate rows in '{selected_column}': {duplicate_rows}")

    # Validity Check: For demonstration, assuming a column with boolean values ('completed' from earlier dataset)
    if 'completed' in df.columns:
        st.sidebar.header("Validity Check")
        validity = perform_validity_check(df, 'completed', [True, False])
        st.sidebar.write(f"Validity (boolean): {validity:.2f}%")

    # Data Quality Metrics Visualization
    st.subheader("Data Quality Metrics")

    # Create a DataFrame for quality results
    metrics_data = {
        "Metric": ["Completeness", "Duplicate Rows", "Validity (completed field)"],
        "Value": [f"{completeness:.2f}%", duplicate_rows, f"{validity:.2f}%" if 'completed' in df.columns else "N/A"]
    }
    metrics_df = pd.DataFrame(metrics_data)

    # Display the data quality metrics as a table
    st.table(metrics_df)

    # Visualizations
    st.subheader("Visualizations")

    # Completeness Visualization
    fig_completeness = px.pie(
        names=["Complete Data", "Missing Data"],
        values=[df.size - missing_values, missing_values],
        title="Completeness of Data"
    )
    st.plotly_chart(fig_completeness, use_container_width=True)

    # Uniqueness Visualization
    fig_uniqueness = px.bar(
        x=["Unique Rows", "Duplicate Rows"],
        y=[len(df) - duplicate_rows, duplicate_rows],
        title=f"Uniqueness Check for '{selected_column}'"
    )
    st.plotly_chart(fig_uniqueness, use_container_width=True)

    # Conditional validity visualization
    if 'completed' in df.columns:
        fig_validity = px.pie(
            names=["Valid Boolean", "Invalid"],
            values=[df['completed'].isin([True, False]).sum(), len(df) - df['completed'].isin([True, False]).sum()],
            title="Validity of 'completed' field"
        )
        st.plotly_chart(fig_validity, use_container_width=True)

else:
    st.write("Please upload a CSV file to start the analysis.")
