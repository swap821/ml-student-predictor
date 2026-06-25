"""
validators.py — Input validation helpers for the ML Student Predictor API.

Centralizes all request validation logic so routes stay clean and
validation rules are reusable and testable.
"""

from typing import Dict, List, Tuple, Optional


# Features expected by the trained model (order matters)
REQUIRED_FEATURES = [
    "study_hours_per_week",
    "attendance_rate",
    "previous_grade",
    "extracurricular_activities",
    "parental_education",
    "school_type",
    "gender",
    "distance_to_school",
]

# Valid ranges for numeric features
NUMERIC_RANGES = {
    "study_hours_per_week": (0, 80),
    "attendance_rate": (0, 100),
    "previous_grade": (0, 100),
    "distance_to_school": (0, 50),
}

# Valid categorical values
CATEGORICAL_VALUES = {
    "extracurricular_activities": [0, 1],
    "parental_education": [0, 1, 2, 3, 4],
    "school_type": [0, 1],
    "gender": [0, 1],
}


def validate_prediction_input(data: dict) -> Tuple[bool, Optional[str]]:
    """
    Validate incoming prediction request payload.

    Returns:
        (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"

    # Check all required fields are present
    missing = [f for f in REQUIRED_FEATURES if f not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    # Check for unexpected extra fields
    extra = [f for f in data if f not in REQUIRED_FEATURES]
    if extra:
        return False, f"Unexpected fields: {', '.join(extra)}"

    # Validate numeric ranges
    for field, (min_val, max_val) in NUMERIC_RANGES.items():
        value = data[field]
        if not isinstance(value, (int, float)):
            return False, f"'{field}' must be a number"
        if not (min_val <= value <= max_val):
            return False, f"'{field}' must be between {min_val} and {max_val}"

    # Validate categorical values
    for field, valid_values in CATEGORICAL_VALUES.items():
        value = data[field]
        if value not in valid_values:
            return False, f"'{field}' must be one of {valid_values}"

    return True, None


def sanitize_input(data: dict) -> dict:
    """
    Sanitize and normalize input values before feeding to the model.
    Rounds floats to avoid precision issues.
    """
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, float):
            sanitized[key] = round(value, 2)
        else:
            sanitized[key] = value
    return sanitized


def validate_batch_input(items: list) -> Tuple[bool, Optional[str], List[dict]]:
    """
    Validate a batch of prediction inputs.

    Returns:
        (is_valid, error_message, sanitized_items)
    """
    if not isinstance(items, list):
        return False, "Batch input must be a JSON array", []

    if len(items) == 0:
        return False, "Batch cannot be empty", []

    if len(items) > 100:
        return False, "Batch size exceeds maximum of 100", []

    sanitized_items = []
    for idx, item in enumerate(items):
        valid, error = validate_prediction_input(item)
        if not valid:
            return False, f"Item {idx}: {error}", []
        sanitized_items.append(sanitize_input(item))

    return True, None, sanitized_items
