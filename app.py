
import streamlit as st
import pandas as pd
import json
from io import BytesIO

from src.pipeline.cleaner import (
    clean_data,
    fill_missing_values,
    drop_invalid_required_rows
)
from src.pipeline.transformer import transform_data
from src.pipeline.config import load_config
from src.pipeline.io import read_data


st.set_page_config(
    page_title="Data Processing Pipeline",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Processing Pipeline")
st.write(
    "Upload CSV or JSON data, or provide an API URL. "
    "The application will clean, transform and validate your data."
)

config = load_config("config/config.yaml")
processing = config.get("processing", {})

st.sidebar.header("Input Settings")

source_type = st.sidebar.selectbox(
    "Choose input source",
    ["CSV", "JSON", "API"]
)

uploaded_file = None
api_url = ""

if source_type in ["CSV", "JSON"]:
    uploaded_file = st.file_uploader(
        "Upload your dataset",
        type=["csv", "json"] if source_type == "CSV" else ["json"]
    )

else:
    api_url = st.text_input("Enter API URL")

if st.button("Process Data", type="primary"):

    try:
        if source_type == "CSV":
            if uploaded_file is None:
                st.warning("Please upload a CSV file.")
                st.stop()

            df = pd.read_csv(BytesIO(uploaded_file.getvalue()))

        elif source_type == "JSON":
            if uploaded_file is None:
                st.warning("Please upload a JSON file.")
                st.stop()

            df = pd.read_json(BytesIO(uploaded_file.getvalue()))

        else:
            if not api_url.strip():
                st.warning("Please enter an API URL.")
                st.stop()

            df = read_data(
                source_type="api",
                url=api_url
            )

        original_rows = len(df)

        st.subheader("Original Data")
        st.dataframe(df, use_container_width=True)

        df = clean_data(
            df=df,
            required_columns=processing.get("required_columns", []),
            missing_values=processing.get("missing_values", {}),
            drop_duplicates=processing.get("drop_duplicates", True)
        )

        df = transform_data(
            df=df,
            numeric_columns=processing.get("numeric_columns", []),
            date_columns=processing.get("date_columns", [])
        )

        df = fill_missing_values(
            df,
            processing.get("missing_values", {})
        )

        df = drop_invalid_required_rows(
            df,
            processing.get("required_columns", [])
        )

        st.subheader("Processing Results")

        col1, col2, col3 = st.columns(3)

        col1.metric("Original Records", original_rows)
        col2.metric("Processed Records", len(df))
        col3.metric("Removed Records", original_rows - len(df))

        st.subheader("Cleaned Data")
        st.dataframe(df, use_container_width=True)

        csv_data = df.to_csv(index=False).encode("utf-8")

        json_data = df.to_json(
            orient="records",
            indent=2,
            date_format="iso"
        ).encode("utf-8")

        st.subheader("Download Results")

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "Download CSV",
                data=csv_data,
                file_name="processed_data.csv",
                mime="text/csv"
            )

        with col2:
            st.download_button(
                "Download JSON",
                data=json_data,
                file_name="processed_data.json",
                mime="application/json"
            )

        st.success("Data processing completed successfully!")

    except Exception as e:
        st.error(f"Processing failed: {e}")
