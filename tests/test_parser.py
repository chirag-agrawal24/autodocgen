import os
import pytest
from autodocgen.parser import parse_file

def test_parser_reads_function():
    sample_path = os.path.join(os.path.dirname(__file__), "../test_files/sample.py")
    functions = parse_file(sample_path)

    assert len(functions) == 1
    assert functions[0]["name"] == "add"
    assert "No docstring available." in functions[0]["docstring"]
