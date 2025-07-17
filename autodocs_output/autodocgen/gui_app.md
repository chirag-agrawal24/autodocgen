# autodocgen/gui_app.py

> AI summary failed.


---


## Class: `AutoDocGUI`

No class docstring available.


### Method: `__init__`
- **Arguments**: ['self', 'root']
- **Returns**: None

Initializes the application instance, setting the root window for the graphical user interface. 

Args:
    self (object): A reference to the current instance of the class
    root (tkinter.Tk): The root window of the application

### Method: `setup_ui`
- **Arguments**: ['self']
- **Returns**: None

Sets up the user interface for the application, initializing all necessary tkinter components and configuring the visual layout.

### Method: `browse_project`
- **Arguments**: ['self']
- **Returns**: None

Browses the project directory to select a folder containing Python files for documentation generation.

Args:
    self: A reference to the current instance of the class

Returns:
    None

Note:
    This function utilizes tkinter's filedialog to prompt the user for a directory selection.

### Method: `browse_output`
- **Arguments**: ['self']
- **Returns**: None

Browses the generated output files and allows the user to select and view them.
 
Args:
    self: A reference to the current instance of the class
 
Returns:
    None
    Opens the file dialog for the user to browse and select the generated output files.

### Method: `add_ignore_folder`
- **Arguments**: ['self']
- **Returns**: None

Adds a folder to be ignored by the autodocgen tool, allowing users to exclude specific directories from documentation generation.

### Method: `clear_ignore_folders`
- **Arguments**: ['self']
- **Returns**: None

Clears the ignore folders list, effectively removing any previously set folders to be ignored by the documentation generation process.

### Method: `generate_docstrings`
- **Arguments**: ['self']
- **Returns**: None

Generate docstrings for the current project using automated tools.

Args:
    self: A reference to the current instance

Returns:
    None

Notes:
    This function leverages the autodocgen library to parse Python files, 
    generate documentation, and export it as a PDF or README file. 
    Additionally, it can utilize AI-powered tools to generate a README.

### Method: `on_tree_select`
- **Arguments**: ['self', 'event']
- **Returns**: None

Handles the event triggered when a tree item is selected, allowing users to interact with the tree view and access related functionality. 

Args:
    self (object): A reference to the instance of the class.
    event (object): The event object triggered by the tree item selection.

### Method: `reject_current_docstring`
- **Arguments**: ['self']
- **Returns**: None

Rejects the current docstring, allowing the user to restart the docstring generation process. 

Args:
    self: A reference to the current instance of the class. 

Returns:
    None

### Method: `save_final_docstrings`
- **Arguments**: ['self']
- **Returns**: None

Saves the final docstrings after all processing and generation steps have been completed. 

Args:
    self: A reference to the current instance of the class 

Note: This function is part of a class due to the self argument, likely used in a GUI application for generating documentation with autodocgen and tkinter.

### Method: `generate_docs`
- **Arguments**: ['self', 'fmt']
- **Returns**: None

Generate documentation in the specified format.

Args:
    fmt (str): The format of the documentation to be generated.

Returns:
    None

Raises:
    ValueError: If the format is not supported.

### Method: `generate_pdf`
- **Arguments**: ['self']
- **Returns**: None

Generates a PDF document based on the current state of the application, utilizing the autodocgen library to parse and export documentation.

### Method: `generate_readme`
- **Arguments**: ['self']
- **Returns**: None

Generates a README file based on the project's documentation, providing an overview of the project and its components.




---


## Function: `launch`
- **Arguments**: []
- **Returns**: None

Launches the autodocgen application, providing a graphical interface to parse Python files, generate documentation, and export to various formats.

Args:
    None

Returns:
    None

Notes:
    This function utilizes tkinter for the graphical interface and integrates various autodocgen modules for parsing, generating, and exporting documentation.

