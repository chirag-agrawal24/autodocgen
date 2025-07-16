import argparse
import os
import sys

from autodocgen.runner import run_documentation_tool


def main():
    parser = argparse.ArgumentParser(description="📘 Generate documentation from Python source code.")
    subparsers = parser.add_subparsers(dest="command")

    # CLI Mode
    cli_parser = subparsers.add_parser("run", help="Run in CLI mode")
    cli_parser.add_argument("--path", type=str, required=True, help="Path to the Python project directory.")
    cli_parser.add_argument("--output-dir", type=str, default="docs", help="Directory to write the documentation.")
    cli_parser.add_argument("--fmt", choices=["markdown", "html"], default="markdown", help="Output format.")
    cli_parser.add_argument("--use-ai", action="store_true", help="Use AI to generate docstrings and file summaries.")
    cli_parser.add_argument("--pdf", action="store_true", help="Export HTML docs to PDF.")
    cli_parser.add_argument("--readme", action="store_true", help="Generate README.md for the project.")
    cli_parser.add_argument("--inject-docs", action="store_true", help="Inject AI-generated docstrings into code.")
    cli_parser.add_argument("--inplace", action="store_true", help="Modify original source files (DANGEROUS).")
    cli_parser.add_argument("--force", action="store_true", help="Force overwrite existing docstrings.")
    cli_parser.add_argument("--diff", action="store_true", help="Show diff of injected docstrings.")
    cli_parser.add_argument(
    "--ignore",
    action="append",
    default=[],
    help="Folders to ignore (can be specified multiple times)."
)


    # GUI Mode
    subparsers.add_parser("gui", help="Launch the GUI")

    args = parser.parse_args()

    if args.command == "gui":
        from autodocgen.gui_app import launch
        launch()

    elif args.command == "run":
        project_path = os.path.abspath(args.path)
        output_dir = os.path.abspath(args.output_dir)

        if not os.path.exists(project_path):
            print(f"❌ Error: path '{project_path}' does not exist.")
            sys.exit(1)

        os.makedirs(output_dir, exist_ok=True)
        print(args.ignore)
        run_documentation_tool({
            "path": project_path,
            "output": output_dir,
            "fmt": args.fmt,
            "use_ai": args.use_ai,
            "pdf": args.pdf,
            "readme": args.readme,
            "inject_docs": args.inject_docs,
            "inplace": args.inplace,
            "force": args.force,
            "diff": args.diff,
            "ignore":args.ignore
        }, logger=print)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
