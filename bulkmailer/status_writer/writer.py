"""Status writer for saving updated files with status tracking"""
import os
import pandas as pd
from ..file_loader import FileData


def save_file_with_status(file_data: FileData, inplace: bool = False) -> str:
    """
    Save the file with updated status column.

    Args:
        file_data: FileData object containing the dataframe with status updates
        inplace: If True and file is Excel, overwrite the original file.
                 CSV files are always overwritten.

    Returns:
        Path to the saved file

    Raises:
        IOError: If file cannot be saved
    """
    df = file_data.df
    file_path = file_data.file_path
    file_type = file_data.file_type

    try:
        if file_type == 'csv':
            # CSV always overwrites the original
            df.to_csv(file_path, index=False)
            return file_path
        else:
            # Excel handling
            if inplace:
                # Overwrite original
                df.to_excel(file_path, index=False, engine='openpyxl')
                return file_path
            else:
                # Create new file with _updated suffix
                base_name, ext = os.path.splitext(file_path)
                new_path = f"{base_name}_updated{ext}"

                # Handle case where _updated file already exists
                counter = 1
                while os.path.exists(new_path):
                    new_path = f"{base_name}_updated_{counter}{ext}"
                    counter += 1

                df.to_excel(new_path, index=False, engine='openpyxl')
                return new_path

    except Exception as e:
        raise IOError(f"Failed to save file: {str(e)}")
