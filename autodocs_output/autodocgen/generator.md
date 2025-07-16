# autodocgen/generator.py

> AI summary failed.


---


## Function: `export_pdf`
- **Arguments**: ['output_dir']
- **Returns**: None

Export documentation as a PDF file to the specified output directory.

Parameters
output_dir (str): The directory where the PDF file will be saved.


---


## Function: `export_pdf_simple`
- **Arguments**: ['output_dir']
- **Returns**: None

Export documentation as a PDF to the specified output directory.

 Parameters:
 output_dir (str): The directory where the PDF will be saved. 

 Returns:
 None 

 Raises:
 ImportError: If the weasyprint library is not installed.


---


## Function: `generate_readme`
- **Arguments**: ['project_path', 'file_descriptions', 'use_ai']
- **Returns**: None

Generate a README file for a project based on provided file descriptions and optionally utilize AI.

### Parameters
* project_path: The path to the project directory.
* file_descriptions: Descriptions of the files in the project.
* use_ai: A flag indicating whether to use AI for generating the README.

### Returns 
No return value.


---


## Function: `markdown_filter`
- **Arguments**: ['text']
- **Returns**: None

Convert markdown text to HTML format.

### Parameters

* text (str): The markdown text to be converted.

### Returns

* str: The HTML representation of the input markdown text.


---


## Function: `render_template`
- **Arguments**: ['template_name', 'context', 'output_path', 'fmt']
- **Returns**: None

Render a template with given context and save it to a file.

 Args:
     template_name (str): Name of the template to render.
     context (dict): Dictionary of variables to pass to the template.
     output_path (str): Path to save the rendered template.
     fmt (str): Format of the output file.

 Returns:
     None


---


## Function: `generate_docs`
- **Arguments**: ['grouped', 'file_descriptions', 'output_dir', 'fmt', 'soucre_path']
- **Returns**: None

Generate documentation for a project based on provided information
  Args:
    grouped: Grouped functions by file
    file_descriptions: Descriptions of files
    output_dir: Output directory for generated documentation
    fmt: Format of the documentation
    source_path: Path to source code files
  Returns: 
    None

