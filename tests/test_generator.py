import os
from autodocgen.generator import generate_docs

def test_generator_creates_markdown(tmp_path):
    functions = [
        {"name": "hello", "args": ["name"], "docstring": "Says hello", "file": "test.py"}
    ]
    generate_docs(functions, output_dir=tmp_path, fmt="markdown")

    output_file = tmp_path / "documentation.md"
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "Documentation" in content
    assert "hello(name)" in content
