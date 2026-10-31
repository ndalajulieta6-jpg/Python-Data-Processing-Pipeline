import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.pipeline.cleaner import clean_data
from src.pipeline.transformer import transform_data


class TestDataPipeline(unittest.TestCase):
    def test_cleaning_removes_duplicates_and_normalizes_email(self):
        df = pd.DataFrame(
            [
                {"customer_id": 1, "name": " Alice ", "email": "ALICE@EXAMPLE.COM", "age": None},
                {"customer_id": 1, "name": " Alice ", "email": "ALICE@EXAMPLE.COM", "age": None},
            ]
        )

        result = clean_data(
            df,
            required_columns=["customer_id", "name", "email"],
            missing_values={"age": 0},
            drop_duplicates=True,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result.loc[0, "name"], "Alice")
        self.assertEqual(result.loc[0, "email"], "alice@example.com")

    def test_numeric_and_date_conversion(self):
        df = pd.DataFrame(
            [
                {"age": "25", "monthly_spend": "100.50", "signup_date": "2026/01/10"},
                {"age": "bad", "monthly_spend": "bad", "signup_date": "not-a-date"},
            ]
        )

        result = transform_data(
            df,
            numeric_columns=["age", "monthly_spend"],
            date_columns=["signup_date"],
        )

        self.assertEqual(result.loc[0, "age"], 25)
        self.assertEqual(result.loc[0, "monthly_spend"], 100.50)
        self.assertEqual(result.loc[0, "signup_date"], "2026-01-10")
        self.assertTrue(pd.isna(result.loc[1, "age"]))
        self.assertTrue(pd.isna(result.loc[1, "monthly_spend"]))
        self.assertTrue(pd.isna(result.loc[1, "signup_date"]))

    def test_missing_required_columns_raise_error(self):
        df = pd.DataFrame([{"name": "Alice"}])

        with self.assertRaises(ValueError):
            clean_data(
                df,
                required_columns=["customer_id", "name"],
                missing_values={},
            )


if __name__ == "__main__":
    unittest.main()
