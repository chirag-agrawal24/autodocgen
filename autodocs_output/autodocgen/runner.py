import os
from autodocgen.parser import parse_python_files
from autodocgen.generator import generate_docs, generate_readme, export_pdf
from autodocgen.inject_docstrings import inject_into_file
from autodocgen.logger import SimpleLogger
logger = SimpleLogger(name='autodocgen', log_file='autodocgen.log')


def should_ignore(path, ignore_list):
    return any(os.path.commonpath([path, os.path.abspath(ign)]) == os.path.
        abspath(ign) for ign in ignore_list)


def run_documentation_tool(args: dict, logger=logger):
    """
    Run the full documentation pipeline.
    
    Args:
        args (dict): Dictionary of options.
        logger (callable): Logging function (default is print).
    """
    path = args.get('path')
    output_dir = args.get('output')
    fmt = args.get('fmt', 'markdown')
    use_ai = args.get('use_ai', False)
    export_as_pdf = args.get('pdf', False)
    generate_readme_flag = args.get('readme', False)
    inject_docs = args.get('inject_docs', False)
    inplace = args.get('inplace', False)
    force = args.get('force', False)
    show_diff = args.get('diff', False)
    ignore_paths = args.get('ignore', [])
    if not os.path.exists(path):
        logger(f"❌ Error: path '{path}' does not exist.")
        return
    os.makedirs(output_dir, exist_ok=True)
    logger(f'Parsing Python files in: {path}')
    logger(f'Output directory: {output_dir}')
    logger(f'Documentation format: {fmt}')
    logger('Ignoring directories: ' + ', '.join(ignore_paths) if
        ignore_paths else 'No directories to ignore')
    grouped, file_descriptions = parse_python_files(path, use_ai=use_ai,
        ignore=ignore_paths)
    if inject_docs:
        logger('Injecting AI docstrings into source files...')
        for root, _, files in os.walk(path):
            if should_ignore(root, ignore_paths):
                continue
            for file in files:
                if file.endswith('.py'):
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, path)
                    dest_file = src_file if inplace else os.path.join(
                        output_dir, rel_path)
                    inject_into_file(src_file, dest_path=dest_file, force=
                        force, show_diff=show_diff)
        logger(
            f"Docstrings injected {'(in-place)' if inplace else 'in copied files'}"
            )
    logger(f'Generating documentation in {fmt} format...')
    if fmt not in ['markdown', 'html']:
        logger(
            f"❌ Unsupported format: {fmt}. Supported formats are 'markdown' and 'html'."
            )
        return
    print(grouped.keys())
    generate_docs(grouped, file_descriptions, output_dir, fmt=fmt,
        soucre_path=path)
    if export_as_pdf and fmt == 'html':
        export_pdf(output_dir)
        logger('PDF export complete.')
    if generate_readme_flag:
        generate_readme(project_path=path, output_path=output_dir,
            file_descriptions=file_descriptions, use_ai=use_ai,
            replace_existing=inplace)
        logger('README.md generated.')
