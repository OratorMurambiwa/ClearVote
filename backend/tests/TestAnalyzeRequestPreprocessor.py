"""Tests for AnalyzeRequestPreprocessor."""

import unittest

from backend.app.AnalyzeRequestPreprocessor import (
    AnalyzeRequestPreprocessor,
    MAX_TEXT_LENGTH,
)


class TestAnalyzeRequestPreprocessor(unittest.TestCase):
    """Tests validation and cleaning of analysis request text."""

    def test_accepts_valid_text(self):
        result = AnalyzeRequestPreprocessor.preprocess_text(
            "This is a political claim."
        )
        self.assertEqual(result, "This is a political claim.")

    def test_removes_extra_whitespace(self):
        result = AnalyzeRequestPreprocessor.preprocess_text(
            "  This   is\n a claim.  "
        )
        self.assertEqual(result, "This is a claim.")

    def test_rejects_empty_text(self):
        with self.assertRaises(ValueError):
            AnalyzeRequestPreprocessor.preprocess_text("")

    def test_rejects_whitespace_only_text(self):
        with self.assertRaises(ValueError):
            AnalyzeRequestPreprocessor.preprocess_text("   ")

    def test_rejects_non_string_input(self):
        with self.assertRaises(ValueError):
            AnalyzeRequestPreprocessor.preprocess_text(None)

    def test_rejects_text_over_limit(self):
        text = "a" * (MAX_TEXT_LENGTH + 1)

        with self.assertRaises(ValueError):
            AnalyzeRequestPreprocessor.preprocess_text(text)

    def test_accepts_text_at_limit(self):
        text = "a" * MAX_TEXT_LENGTH

        result = AnalyzeRequestPreprocessor.preprocess_text(text)

        self.assertEqual(len(result), MAX_TEXT_LENGTH)


if __name__ == "__main__":
    unittest.main()