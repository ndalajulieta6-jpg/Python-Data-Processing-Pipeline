from pathlib import Path

from .cleaner import clean_data, drop_invalid_required_rows, fill_missing_values
from .config import load_config
from .io import read_data, write_data
from .logger import setup_logger
from .transformer import transform_data


class DataPipeline:
    def __init__(self, config_path: str):
        self.config = load_config(config_path)

        logging_config = self.config.get("logging", {})
        self.logger = setup_logger(
            logging_config.get("level", "INFO"),
            logging_config.get("file", "logs/pipeline.log"),
        )

    def run(self) -> str:
        input_config = self.config.get("input", {})
        output_config = self.config.get("output", {})
        processing = self.config.get("processing", {})

        self.logger.info("Starting data pipeline")

        df = read_data(
            source_type=input_config.get("type", "csv"),
            path=input_config.get("path", ""),
            url=input_config.get("url", ""),
        )
        self.logger.info("Loaded %d rows and %d columns", len(df), len(df.columns))

        original_rows = len(df)

        df = clean_data(
            df=df,
            required_columns=processing.get("required_columns", []),
            missing_values=processing.get("missing_values", {}),
            drop_duplicates=processing.get("drop_duplicates", True),
        )
        self.logger.info("Cleaning complete: %d rows remain", len(df))

        df = transform_data(
            df=df,
            numeric_columns=processing.get("numeric_columns", []),
            date_columns=processing.get("date_columns", []),
        )
        self.logger.info("Transformation complete")

        df = fill_missing_values(df, processing.get("missing_values", {}))
        df = drop_invalid_required_rows(
            df, processing.get("required_columns", [])
        )
        self.logger.info("Missing-value handling and final validation complete: %d rows remain", len(df))

        output_type = output_config.get("type", "csv")
        output_path = output_config.get("path", "data/output/processed.csv")

        write_data(df, output_type, output_path)

        self.logger.info(
            "Pipeline finished: %d input rows -> %d output rows",
            original_rows,
            len(df),
        )
        self.logger.info("Output written to %s", output_path)

        return str(Path(output_path))
