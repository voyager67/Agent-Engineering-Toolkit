"""Regression tests for skill metadata boundaries and malformed frontmatter."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_skills import parse_skill_file, validate_skill_file  # noqa: E402


class SkillMetadataBoundaryTests(unittest.TestCase):
    """Exercise metadata length, format, required fields, and parser failures."""

    def write_skill(self, directory: str, frontmatter: str) -> Path:
        path = Path(directory) / "SKILL.md"
        body = "Operational workflow. " * 12
        path.write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")
        return path

    def test_accepts_name_and_description_at_documented_limits(self):
        with tempfile.TemporaryDirectory() as temp:
            frontmatter = f"name: {'a' * 64}\ndescription: {'d' * 1024}"
            path = self.write_skill(temp, frontmatter)
            errors = validate_skill_file(path)
        self.assertEqual(errors, [])

    def test_rejects_name_longer_than_64_characters(self):
        with tempfile.TemporaryDirectory() as temp:
            frontmatter = f"name: {'a' * 65}\ndescription: Valid description."
            path = self.write_skill(temp, frontmatter)
            errors = validate_skill_file(path)
        self.assertTrue(any("name exceeds 64 characters" in error for error in errors))

    def test_rejects_description_longer_than_1024_characters(self):
        with tempfile.TemporaryDirectory() as temp:
            frontmatter = f"name: sample-skill\ndescription: {'d' * 1025}"
            path = self.write_skill(temp, frontmatter)
            errors = validate_skill_file(path)
        self.assertTrue(any("description exceeds 1024 characters" in error for error in errors))

    def test_rejects_name_that_is_not_a_lowercase_hyphenated_slug(self):
        with tempfile.TemporaryDirectory() as temp:
            path = self.write_skill(temp, "name: Invalid_Name\ndescription: Valid description.")
            errors = validate_skill_file(path)
        self.assertTrue(any("lowercase hyphenated slug" in error for error in errors))

    def test_reports_missing_closing_frontmatter_delimiter(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "SKILL.md"
            path.write_text(
                "---\nname: sample-skill\ndescription: A valid description.\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "closing"):
                parse_skill_file(path)

    def test_reports_frontmatter_line_without_key_value_separator(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "SKILL.md"
            path.write_text(
                "---\nname: sample-skill\nthis is malformed\ndescription: Valid.\n---\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "expected key: value"):
                parse_skill_file(path)

    def test_reports_empty_frontmatter_value(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "SKILL.md"
            path.write_text(
                "---\nname: sample-skill\ndescription:\n---\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "key and value are required"):
                parse_skill_file(path)

    def test_reports_missing_required_name_field(self):
        with tempfile.TemporaryDirectory() as temp:
            path = self.write_skill(temp, "description: Valid description.")
            errors = validate_skill_file(path)
        self.assertTrue(any("missing required 'name' field" in error for error in errors))

    def test_reports_missing_required_description_field(self):
        with tempfile.TemporaryDirectory() as temp:
            path = self.write_skill(temp, "name: sample-skill")
            errors = validate_skill_file(path)
        self.assertTrue(any("missing required 'description' field" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
