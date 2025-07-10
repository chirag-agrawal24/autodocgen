import os
from jinja2 import Environment, FileSystemLoader

def generate_docs(functions, output_dir, fmt="markdown"):
    template_file = "default.md.j2" if fmt == "markdown" else "default.html.j2"
    env = Environment(loader=FileSystemLoader(searchpath=os.path.join(os.path.dirname(__file__), "templates")))
    template = env.get_template(template_file)

    output = template.render(functions=functions)

    output_path = os.path.join(output_dir, "documentation." + ("md" if fmt == "markdown" else "html"))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"📄 Documentation written to: {output_path}")
