"""Preprocessing and validation for ClearVote analysis requests."""

MAX_TEXT_LENGTH = 5000


class AnalyzeRequestPreprocessor:
    """Validates and cleans text before it enters the analysis pipeline."""

    @staticmethod
    def preprocess_text(text: str) -> str:
        """Validate and clean submitted text."""

        if not isinstance(text, str):
            raise ValueError("Text must be a string.")

        cleaned_text = " ".join(text.split())

        if not cleaned_text:
            raise ValueError("Text is required.")

        if len(cleaned_text) > MAX_TEXT_LENGTH:
            raise ValueError(
                f"Text exceeds the {MAX_TEXT_LENGTH} character limit."
            )

        return cleaned_text