"""File loader for CSV and Excel files"""
import os
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class FileData:
    """Container for loaded file data"""
    df: pd.DataFrame
    file_path: str
    file_type: str  # 'csv' or 'excel'
    status_column: str


def load_file(file_path: str) -> FileData:
    """
    Load CSV or Excel file and prepare it for processing.

    Args:
        file_path: Path to the CSV or Excel file

    Returns:
        FileData object containing the dataframe and metadata

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is unsupported or required columns are missing
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine file type
    file_ext = os.path.splitext(file_path)[1].lower()

    try:
        if file_ext == '.csv':
            df = pd.read_csv(file_path)
            file_type = 'csv'
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path, engine='openpyxl')
            file_type = 'excel'
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Only CSV and Excel (.xlsx) are supported.")
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")

    # Check for required columns
    if 'email' not in df.columns:
        raise ValueError("Required column 'email' not found in file")
    if 'name' not in df.columns:
        raise ValueError("Required column 'name' not found in file")

    # Remove completely empty rows
    df = df.dropna(how='all')

    # Determine status column name
    status_column = _get_status_column_name(df)

    # Add status column if it doesn't exist
    if status_column not in df.columns:
        df[status_column] = ''

    return FileData(
        df=df,
        file_path=file_path,
        file_type=file_type,
        status_column=status_column
    )


def _get_status_column_name(df: pd.DataFrame) -> str:
    """
    Determine the name for the status column.
    Use 'status', or 'status_1', 'status_2', etc. if 'status' is taken.

    Args:
        df: The dataframe

    Returns:
        The status column name to use
    """
    if 'status' not in df.columns:
        return 'status'

    counter = 1
    while f'status_{counter}' in df.columns:
        counter += 1

    return f'status_{counter}'
