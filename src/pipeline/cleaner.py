import pandas as pd


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def clean_data(
    df: pd.DataFrame,
    required_columns: list[str],
    missing_values: dict,
    drop_duplicates: bool = True,
) -> pd.DataFrame:
    validate_required_columns(df, required_columns)
    cleaned = df.copy()

    for column in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()

    if "email" in cleaned.columns:
        cleaned["email"] = cleaned["email"].str.lower()

    if drop_duplicates:
        cleaned = cleaned.drop_duplicates()

    # Missing values are filled after type conversion in the pipeline so that
    # numeric defaults such as 0 can be safely inserted into numeric columns.
    return cleaned.reset_index(drop=True)


def fill_missing_values(df: pd.DataFrame, missing_values: dict) -> pd.DataFrame:
    result = df.copy()
    for column, value in missing_values.items():
        if column in result.columns:
            result[column] = result[column].fillna(value)
    return result


def drop_invalid_required_rows(df: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
    result = df.copy()
    for column in required_columns:
        if column in result.columns:
            result[column] = result[column].replace(r"^\s*$", pd.NA, regex=True)
    return result.dropna(subset=required_columns).reset_index(drop=True)
