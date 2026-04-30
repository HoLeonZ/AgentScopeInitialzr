"""
Tests for historical bug fixes.

This module ensures that previously discovered bugs do not regress.
Each test corresponds to a bug that was fixed in the past.

Bug References:
- BUG-001: API URL missing /v1
- BUG-002: LoggingWrapperModel missing stream attribute
- BUG-003: F-string escape conflicts in templates
- BUG-004: Missing .format() call for advanced_example
- BUG-005: Log variable not formatted (literal {model_name})
- BUG-006: Redis close() incompatible with newer redis-py
- BUG-007: Redis memory add() crashes on string/dict inputs
"""

import unittest
import re
import ast
from pathlib import Path


class TestBugFixes(unittest.TestCase):
    """Test cases for historical bug fixes in code generation."""

    @classmethod
    def setUpClass(cls):
        """Load source files for testing."""
        cls.engine_path = Path(__file__).parent.parent.parent / "initializr-core" / "initializr_core" / "generator" / "engine.py"
        cls.extensions_path = Path(__file__).parent.parent.parent / "initializr-core" / "initializr_core" / "generator" / "extensions.py"

        with open(cls.engine_path, "r", encoding="utf-8") as f:
            cls.engine_content = f.read()

        with open(cls.extensions_path, "r", encoding="utf-8") as f:
            cls.extensions_content = f.read()

    # ==================== BUG-001: API URL missing /v1 ====================

    def test_bug001_api_url_includes_v1(self):
        """
        BUG-001: Verify that generated code uses /v1/chat/completions in base_url.

        Historical bug: BASE_URL_NORMALIZED stripped /v1/chat/completions but
        the client was appending /chat/completions, resulting in wrong URL.
        """
        # Check that client_kwargs uses + "/v1"
        self.assertIn(
            '+ "/v1"',
            self.extensions_content,
            "BUG-001: client_kwargs should append '/v1' to base_url"
        )

        # Also check the log message uses /v1/chat/completions
        self.assertIn(
            '"/v1/chat/completions"',
            self.extensions_content,
            "BUG-001: Log URL should include /v1/chat/completions"
        )

    # ==================== BUG-002: LoggingWrapperModel missing stream ====================

    def test_bug002_logging_wrapper_has_stream(self):
        """
        BUG-002: Verify LoggingWrapperModel has stream attribute.

        Historical bug: Accessing .stream on LoggingWrapperModel raised AttributeError.
        """
        # Find the LoggingWrapperModel class definition
        self.assertIn(
            "class LoggingWrapperModel",
            self.extensions_content,
            "BUG-002: LoggingWrapperModel class should exist"
        )

        # Check that self.stream is assigned in the class
        self.assertIn(
            "self.stream = ",
            self.extensions_content,
            "BUG-002: LoggingWrapperModel should set self.stream"
        )

    # ==================== BUG-003: F-string escape conflicts ====================

    def test_bug003_no_fstring_in_templates(self):
        """
        BUG-003: Verify templates don't use f-strings that conflict with .format().

        Historical bug: advanced_template contained f-string variables like
        {user_request}, which caused "Replacement index 0 out of range" errors.
        """
        # Find the advanced_template definition
        advanced_template_match = re.search(
            r'advanced_template\s*=\s*r\'\'\'(.*?)\'\'\'',
            self.engine_content,
            re.DOTALL
        )

        self.assertIsNotNone(
            advanced_template_match,
            "BUG-003: advanced_template should be defined as raw string (r''')"
        )

        template_body = advanced_template_match.group(1)

        # Check that f-strings with format placeholders are not used
        # Pattern like f"...{variable}..." where variable is NOT in the .format() call
        # This is a simplified check - looks for f-strings that might cause issues
        fstring_pattern = r'f"[^"]*\{(?!\{)[^}]+\}[^"]*"'
        fstrings_found = re.findall(fstring_pattern, template_body)

        # Filter out benign patterns - only flag actual variable interpolation
        problematic_fstrings = [
            fs for fs in fstrings_found
            if '{user_request}' in fs or '{results_summary}' in fs
            or '{original_request}' in fs or '{results}' in fs
        ]

        self.assertEqual(
            len(problematic_fstrings),
            0,
            f"BUG-003: Template should not contain f-strings with variables: {problematic_fstrings}"
        )

    # ==================== BUG-004: Missing .format() call ====================

    def test_bug004_advanced_example_has_format_call(self):
        """
        BUG-004: Verify advanced_example calls .format() after template definition.

        Historical bug: The .format() call was missing, causing NameError.
        """
        # Find the advanced_example assignment
        pattern = r'advanced_example\s*=\s*advanced_template\.format\('

        self.assertRegex(
            self.engine_content,
            pattern,
            "BUG-004: advanced_example should be assigned from advanced_template.format()"
        )

    # ==================== BUG-005: Log variable not formatted ====================

    def test_bug005_log_variables_use_string_concatenation(self):
        """
        BUG-005: Verify log statements use string concatenation, not f-strings.

        Historical bug: {{model_name}} was interpreted as literal string, not variable.
        """
        # Check that LLM Response log doesn't use f-string with unescaped braces
        # Pattern: should NOT have f"[...{model_name}...]" or {{model_name}}
        bad_patterns = [
            r'logger\.info\s*f\s*\[\s*"[^"]*\{\{model_name\}\}',  # f"..{{model_name}}.."
            r'logger\.info\s*\[\s*"[^"]*\{model_name\}[^"]*"\s*\]',  # Same with single brace
        ]

        for pattern in bad_patterns:
            matches = re.search(pattern, self.extensions_content)
            self.assertIsNone(
                matches,
                f"BUG-005: Log statement should not use literal braces for variables. Found: {matches.group() if matches else 'N/A'}"
            )

        # Verify string concatenation is used instead
        self.assertIn(
            '" + model_name + "',
            self.extensions_content,
            "BUG-005: Should use string concatenation for model_name in logs"
        )

    # ==================== BUG-006: Redis close() compatibility ====================

    def test_bug006_redis_close_has_fallback(self):
        """
        BUG-006: Verify RedisClusterMemory.close() handles newer redis-py versions.

        Historical bug: close_connection_pool parameter not supported in newer redis-py,
        causing TypeError: aclose() got unexpected keyword argument.
        """
        # Check that close method has try-except for TypeError
        self.assertIn(
            "except TypeError:",
            self.extensions_content,
            "BUG-006: close() should catch TypeError for redis-py compatibility"
        )

        # Check that aclose() is called without the problematic parameter
        self.assertIn(
            "await self._client.aclose()",
            self.extensions_content,
            "BUG-006: except block should call aclose() without close_connection_pool"
        )

    # ==================== BUG-007: Redis memory add() handles non-Msg inputs ====================

    def test_bug007_redis_memory_add_handles_strings(self):
        """
        BUG-007: Verify RedisClusterMemory.add() handles string and dict inputs.

        Historical bug: AgentScope passes raw strings to memory.add(), causing
        AttributeError: 'str' object has no attribute 'id'.
        """
        # Check that add() handles string input
        self.assertIn(
            'isinstance(memories, str)',
            self.extensions_content,
            "BUG-007: add() should handle string input"
        )

        # Check that strings are converted to Msg objects
        self.assertIn(
            'Msg(name="user", content=memories, role="user")',
            self.extensions_content,
            "BUG-007: String should be converted to Msg object"
        )

        # Check that add() handles dict input
        self.assertIn(
            'isinstance(memories, dict)',
            self.extensions_content,
            "BUG-007: add() should handle dict input"
        )

        # Check that dicts are converted using Msg.from_dict
        self.assertIn(
            'Msg.from_dict',
            self.extensions_content,
            "BUG-007: Dict should be converted using Msg.from_dict"
        )


class TestGeneratedCodeTemplates(unittest.TestCase):
    """Test that generated code templates produce valid Python."""

    def test_advanced_template_is_valid_python(self):
        """
        Verify that the advanced_template, when formatted, produces valid Python code.
        """
        # Read the source file and extract the template
        engine_path = Path(__file__).parent.parent.parent / "initializr-core" / "initializr_core" / "generator" / "engine.py"

        with open(engine_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract the advanced_template (it's a raw string starting with r''')
        import re
        match = re.search(r"advanced_template\s*=\s*r'''(.*?)'''", content, re.DOTALL)
        self.assertIsNotNone(match, "advanced_template should exist")

        template_body = match.group(1)

        # Format the template like the generator does
        formatted = template_body.format(
            name="test_project",
            package_name="test_project"
        )

        # Parse it as Python AST
        try:
            ast.parse(formatted)
        except SyntaxError as e:
            self.fail(f"Generated advanced_multiagent.py template is invalid Python: {e}")


if __name__ == "__main__":
    unittest.main()
