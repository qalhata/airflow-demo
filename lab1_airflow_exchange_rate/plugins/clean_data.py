import os
import pandas as pd
import json
import logging

def clean_data(input_path: str, output_dir: str):
    """
    Reads raw exchange rate JSON data, cleans it, and saves it to a partitioned CSV file.

    :param input_path: The path to the input JSON file.
    :param output_dir: The base directory for the partitioned output.
    """
    logging.info(f"Starting data cleaning for file: {input_path}")
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error(f"Input file not found at {input_path}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from {input_path}")
        raise

    if not data:
        logging.warning("Input JSON data is empty. Exiting.")
        return

    # Convert the dictionary of rates into a DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    logging.info(f"Successfully loaded {len(df)} records into DataFrame.")

    # The date is the same for all rows; extract it for partitioning and drop the redundant column.
    rate_date_str = df['date'].iloc[0] if not df.empty else None
    df = df.drop(columns=['name', 'date'])
    df.index.name = 'target_currency_code'

    # Get the current date components
    try:
        partition_date = pd.to_datetime(rate_date_str)
    except (TypeError, ValueError):
        logging.warning("Could not parse date from file, using current date for partitioning.")
        partition_date = pd.Timestamp.now()

    # Create the directory path if it doesn't exist
    partitioned_path = os.path.join(output_dir, str(partition_date.year), str(partition_date.month), str(partition_date.day))
    os.makedirs(partitioned_path, exist_ok=True)
    logging.info(f"Ensured output directory exists: {partitioned_path}")

    # Save the cleaned data to a new file
    output_filepath = os.path.join(partitioned_path, 'xrate_cleansed.csv')
    df.to_csv(output_filepath)
    logging.info(f"Successfully saved cleaned data to {output_filepath}")