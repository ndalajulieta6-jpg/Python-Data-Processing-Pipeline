import pandas as pd


def transform_data(
    df: pd.DataFrame,
    numeric_columns: list[str],
    date_columns: list[str],
) -> pd.DataFrame:
    transformed = df.copy()

    for column in numeric_columns:
        if column in transformed.columns:
            transformed[column] = pd.to_numeric(
                transformed[column], errors="coerce"
            )

    for column in date_columns:
        if column in transformed.columns:
            transformed[column] = pd.to_datetime(
                transformed[column], errors="coerce", format="mixed"
            ).dt.strftime("%Y-%m-%d")

    return transformed
