from pathlib import Path
import pandas as pd
import requests


def read_data(source_type: str, path: str = "", url: str = "") -> pd.DataFrame:
    source_type = source_type.lower()

    if source_type == "csv":
        return pd.read_csv(path)

    if source_type == "json":
        return pd.read_json(path)

    if source_type == "api":
        if not url:
            raise ValueError("API input requires a URL.")

        response = requests.get(url, timeout=30)
        response.raise_for_status()
        payload = response.json()

        if isinstance(payload, list):
            records = payload
        elif isinstance(payload, dict) and isinstance(payload.get("data"), list):
            records = payload["data"]
        else:
            raise ValueError("API response must be a JSON list or an object containing a 'data' list.")

        return pd.DataFrame(records)

    raise ValueError(f"Unsupported input type: {source_type}")


def write_data(df: pd.DataFrame, output_type: str, path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_type = output_type.lower()

    if output_type == "csv":
        df.to_csv(output_path, index=False)
    elif output_type == "json":
        df.to_json(output_path, orient="records", indent=2, date_format="iso")
    else:
        raise ValueError(f"Unsupported output type: {output_type}")
