"""Template engine for replacing placeholders with row data"""
import re
from typing import Dict, List, Tuple


def extract_placeholders(template: str) -> List[str]:
    """
    Extract all placeholders from a template string.

    Args:
        template: String containing placeholders in {column_name} format

    Returns:
        List of placeholder names (without braces)
    """
    pattern = r'\{(\w+)\}'
    return re.findall(pattern, template)


def validate_placeholders(template: str, available_columns: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate that all placeholders in the template exist as columns.

    Args:
        template: Template string with placeholders
        available_columns: List of available column names

    Returns:
        Tuple of (is_valid, missing_placeholders)
    """
    placeholders = extract_placeholders(template)
    missing = [p for p in placeholders if p not in available_columns]
    return len(missing) == 0, missing


def render_template(template: str, row_data: Dict[str, any]) -> Tuple[str, bool, List[str]]:
    """
    Render a template by replacing placeholders with values from row_data.

    Args:
        template: Template string with {placeholder} format
        row_data: Dictionary mapping column names to values

    Returns:
        Tuple of (rendered_string, success, missing_keys)
        - rendered_string: The template with placeholders replaced
        - success: True if all placeholders were successfully replaced
        - missing_keys: List of placeholder keys that were missing or had null values
    """
    placeholders = extract_placeholders(template)
    missing_keys = []
    rendered = template

    for placeholder in placeholders:
        if placeholder not in row_data:
            missing_keys.append(placeholder)
        else:
            value = row_data[placeholder]
            # Check for null/NaN values
            if value is None or (isinstance(value, float) and pd.isna(value)):
                missing_keys.append(placeholder)
            else:
                # Replace the placeholder with the value
                rendered = rendered.replace(f'{{{placeholder}}}', str(value))

    success = len(missing_keys) == 0
    return rendered, success, missing_keys


# Import pandas for NaN checking
import pandas as pd
