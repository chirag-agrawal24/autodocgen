import click
import os

from .parser import parse_python_files
from .generator import generate_docs

@click.command()
@click.option('--input', '-i', 'input_dir', required=True, help='Path to directory with .py files')
@click.option('--output', '-o', 'output_dir', default='docs', show_default=True, help='Output directory for documentation')
@click.option('--format', '-f', 'doc_format', type=click.Choice(['markdown', 'html']), default='markdown', show_default=True, help='Output format')
@click.option('--use-ai', is_flag=True, help='Use AI (Groq) to generate missing docstrings')
def main(input_dir, output_dir, doc_format, use_ai):
    """📘 AutoDocGen: Generate documentation from Python code"""
    click.echo("🚀 Starting AutoDocGen...")

    if not os.path.isdir(input_dir):
        click.echo("❌ Input directory does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Parse all Python files
    click.echo(f"🔍 Parsing Python files in: {input_dir}")
    functions = parse_python_files(input_dir, use_ai=use_ai)

    # Step 2: Generate Documentation
    click.echo(f"📝 Generating {doc_format} documentation...")
    generate_docs(functions, output_dir, fmt=doc_format)

    click.echo("✅ Done!")

if __name__ == "__main__":
    main()
