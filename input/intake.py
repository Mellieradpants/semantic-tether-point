
from typing import Dict


class InputValidationError(Exception):
    pass


def prepare_input(raw_text: str) -> Dict:
    """
    Layer 1 — Input

    Responsibilities:
    - Validate input exists
    - Normalize input shape
    - Pass raw content forward unchanged

    No parsing
    No interpretation
    No restructuring
    """

    # Validate presence
    if raw_text is None:
        raise InputValidationError("Input text is required")

    # Normalize
    text = raw_text.strip()

    if not text:
        raise InputValidationError("Input text is empty")

    # Detect basic type (non-inferential, structural only)
    input_type = detect_input_type(text)

    return {
        "raw_text": text,
        "input_type": input_type
    }


def detect_input_type(text: str) -> str:
    """
    Deterministic type detection.
    No inference.
    """

    if text.startswith("<") and text.endswith(">"):
        return "xml"

    if text.startswith("{") and text.endswith("}"):
        return "json"

    if text.startswith("http://") or text.startswith("https://"):
        return "url"

    return "text"
