# Python Data Processing Pipeline

A small, production-style Python data processing pipeline that reads raw data from **CSV, JSON, or an HTTP API**, cleans and transforms it, handles missing values and type conversions, logs each stage, and writes structured output.

## Features

- CSV, JSON, and API input sources
- Missing-value handling
- Type conversion and validation
- Duplicate removal
- Whitespace/case normalization
- Invalid-record handling without crashing the whole pipeline
- Configurable input/output paths and processing rules
- Console + rotating file logging
- Sample input/output data
- Unit tests
- Command-line entry point

## Project structure

```text
python_data_pipeline/
├── config/
│   └── config.yaml
├── data/
│   ├── input/
│   │   └── sample_customers.csv
│   └── output/
│       └── processed_customers.csv
├── logs/
├── src/
│   └── pipeline/
│       ├── __init__.py
│       ├── cleaner.py
│       ├── config.py
│       ├── io.py
│       ├── logger.py
│       ├── pipeline.py
│       └── transformer.py
├── tests/
│   └── test_pipeline.py
├── .gitignore
├── requirements.txt
└── run_pipeline.py
```

## Requirements

- Python 3.10+
- pip

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/python-data-pipeline.git
cd python-data-pipeline
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the sample pipeline

```bash
python run_pipeline.py
```

The processed file will be written to:

```text
data/output/processed_customers.csv
```

A log file will be created in:

```text
logs/pipeline.log
```

## Configuration

Edit `config/config.yaml` to change the source and processing rules.

Example:

```yaml
input:
  type: csv
  path: data/input/sample_customers.csv
  url: ""

output:
  type: csv
  path: data/output/processed_customers.csv

processing:
  drop_duplicates: true
  required_columns:
    - customer_id
    - name
    - email
    - age
    - monthly_spend
  missing_values:
    age: 0
    monthly_spend: 0.0
  numeric_columns:
    - age
    - monthly_spend
  date_columns:
    - signup_date

logging:
  level: INFO
  file: logs/pipeline.log
```

### API input

To use an API, change the input section:

```yaml
input:
  type: api
  path: ""
  url: https://example.com/api/customers
```

The API is expected to return either:

- a JSON array of records, or
- an object containing a list under `data`.

## Processing rules

The pipeline:

1. Reads the configured source.
2. Verifies required columns.
3. Removes duplicate records when enabled.
4. Trims text fields.
5. Normalizes email addresses to lowercase.
6. Converts numeric columns safely.
7. Converts date columns to ISO dates.
8. Replaces configured missing values.
9. Drops rows that are still invalid in required fields.
10. Writes structured output.
11. Logs useful processing statistics.

Invalid numeric/date values become missing rather than crashing the pipeline.

## Running tests

```bash
python -m unittest discover -s tests -v
```

## Example

Input:

```csv
customer_id,name,email,age,monthly_spend,signup_date
1001, Alice Smith ,ALICE@EXAMPLE.COM,25,1250.50,2026-01-10
1002,Bob Jones,bob@example.com,,850,2026-02-05
1002,Bob Jones,bob@example.com,,850,2026-02-05
1003,Charlie Brown,invalid-email,not-a-number,500,invalid-date
```

The pipeline removes the duplicate, cleans text, converts numeric/date fields, fills configured missing numeric values, and removes records that remain invalid.

## Extending the project

The source is intentionally modular:

- `io.py` handles input/output.
- `cleaner.py` handles data cleaning.
- `transformer.py` handles transformations.
- `config.py` handles YAML configuration.
- `logger.py` handles logging.
- `pipeline.py` coordinates the workflow.

This makes it straightforward to add Excel/database inputs, additional validation rules, or other output formats later.
