import argparse
import logging
from pathlib import Path

import pandas as pd

# Create logs folder if it doesn't exist
Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/converter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def convert_csv_to_excel(input_file, output_file):
    try:
        print("Reading CSV file...")

        df = pd.read_csv(input_file)

        print("Cleaning data...")

        # Fill missing values
        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].fillna(0)
            else:
                df[column] = df[column].fillna("N/A")

        # Rename columns
        df.columns = [col.strip().replace("_", " ").title() for col in df.columns]

        # Parse date columns
        for column in df.columns:
            if "Date" in column:
                df[column] = pd.to_datetime(df[column], errors="coerce")

        print("Saving Excel file...")

        df.to_excel(output_file, index=False)

        logging.info(f"Converted {input_file} -> {output_file}")

        print(f"✅ Successfully saved to {output_file}")

    except FileNotFoundError:
        print("❌ Input file not found.")
        logging.error("Input file not found.")

    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CSV to Excel Converter"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input CSV file"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output Excel file"
    )

    args = parser.parse_args()

    Path("output").mkdir(exist_ok=True)

    convert_csv_to_excel(args.input, args.output)