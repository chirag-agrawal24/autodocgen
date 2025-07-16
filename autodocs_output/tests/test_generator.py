import os
from autodocgen.generator import generate_docs


def test_generator_creates_markdown(tmp_path):
    """Tests that the test generator successfully creates a markdown file in the specified temporary directory. 
Verifies the functionality of the test generator's markdown creation. 
tmp_path is a pytest fixture providing a temporary directory for testing."""
    functions = [{'name': 'hello', 'args': ['name'], 'docstring':
        'Says hello', 'file': 'test.py'}]
    generate_docs(functions, output_dir=tmp_path, fmt='markdown')
    output_file = tmp_path / 'documentation.md'
    assert output_file.exists()
    content = output_file.read_text(encoding='utf-8')
    assert 'Documentation' in content
    assert 'hello(name)' in content
