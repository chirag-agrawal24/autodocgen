import os
from autodocgen.parser import parse_python_files
from autodocgen.generator import generate_docs, generate_readme, export_pdf
from autodocgen.inject_docstrings import inject_into_file

def run_documentation_tool(args: dict, logger=print):
    """
    Run the full documentation pipeline.
    
    Args:
        args (dict): Dictionary of options.
        logger (callable): Logging function (default is print).
    """
    path = args.get("path")
    output_dir = args.get("output")
    fmt = args.get("fmt", "markdown")
    use_ai = args.get("use_ai", False)
    export_as_pdf = args.get("pdf", False)
    generate_readme_flag = args.get("readme", False)
    inject_docs = args.get("inject_docs", False)
    inplace = args.get("inplace", False)
    force = args.get("force", False)
    show_diff = args.get("diff", False)

    if not os.path.exists(path):
        logger(f"❌ Error: path '{path}' does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)

    logger(f"🔍 Parsing Python files in: {path}")
    grouped, file_descriptions = parse_python_files(path, use_ai=use_ai)

    logger(f"🛠️ Generating documentation in {fmt} format...")
    generate_docs(grouped, file_descriptions, output_dir, fmt=fmt)

    if export_as_pdf and fmt == "html":
        export_pdf(output_dir)
        logger("📄 PDF export complete.")

    if generate_readme_flag:
        generate_readme(path, file_descriptions, use_ai=use_ai)
        logger("📘 README.md generated.")

    if inject_docs:
        logger("🧠 Injecting AI docstrings into source files...")
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, path)
                    dest_file = src_file if inplace else os.path.join(output_dir, rel_path)

                    inject_into_file(
                        src_file,
                        dest_path=dest_file,
                        force=force,
                        show_diff=show_diff
                    )

        logger(f"✅ Docstrings injected {'(in-place)' if inplace else 'in copied files'}")
