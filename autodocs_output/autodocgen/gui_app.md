# autodocgen/gui_app.py

> AI summary failed.


---


## Class: `AutoDocGUI`

No class docstring available.


### Method: `__init__`
- **Arguments**: ['self', 'root']
- **Returns**: None

Initializes the object with the given root window.

 Args:
     self: The instance of the class.
     root: The root window of the application.

### Method: `setup_ui`
- **Arguments**: ['self']
- **Returns**: None

Sets up the user interface for the application.

No arguments are required beyond the instance reference.

This method is responsible for initializing and configuring the UI components.

It does not return any value.

### Method: `browse_project`
- **Arguments**: ['self']
- **Returns**: None

Opens a file dialog for project selection and generates documentation 
based on the chosen project's Python files.

### Method: `browse_output`
- **Arguments**: ['self']
- **Returns**: None

Opens a file dialog for browsing and selecting output files or directories.

### Method: `add_ignore_folder`
- **Arguments**: ['self']
- **Returns**: None

Adds a folder to the ignore list, preventing documentation generation for its contents.

### Method: `clear_ignore_folders`
- **Arguments**: ['self']
- **Returns**: None

Clears the list of folders to be ignored during documentation generation. 
Resets the ignore list to its default state, allowing all folders to be processed.

### Method: `generate_docstrings`
- **Arguments**: ['self']
- **Returns**: None

Generate docstrings for the current object.

### Parameters
* self: The instance of the class this function is part of.

### Returns 
None

### Method: `on_tree_select`
- **Arguments**: ['self', 'event']
- **Returns**: None

Handles the selection of a tree item.

 
Parameters
    event: The event triggered by selecting a tree item.

Returns
    None

### Method: `reject_current_docstring`
- **Arguments**: ['self']
- **Returns**: None

Rejects the current docstring, likely removing or clearing it from the current context.

### Method: `save_final_docstrings`
- **Arguments**: ['self']
- **Returns**: None

Saves the final docstrings to a file, prompting the user for a save location.
 
Parameters
----------
self : object
    The instance of the class this method is part of

Returns
-------
None

### Method: `generate_docs`
- **Arguments**: ['self', 'fmt']
- **Returns**: None

Generate documentation for the given format.

 Args:
     self: A reference to the current instance of the class.
     fmt: The format of the documentation to be generated.

 Returns:
     None

### Method: `generate_pdf`
- **Arguments**: ['self']
- **Returns**: None

Generate a PDF document based on the parsed documentation.

No arguments are required beyond the implicit reference to the class instance (self). 

Alternatively, you could phrase it:
 
Create and export a PDF document based on parsed documentation.

Or 
 Export documentation as a PDF file.

### Method: `generate_readme`
- **Arguments**: ['self']
- **Returns**: None

Generates a README file for the project based on the parsed documentation.

### Parameters
* self: reference to the instance of the class

### Returns
None 

or 

Alternatively if it generates readme and returns path 

### Returns 
str: path to the generated README file 

Please adjust according to actual functionality.




---


## Function: `launch`
- **Arguments**: []
- **Returns**: None

Launch the documentation generation process. 
 No arguments are required for this function. 
 It appears to be an entry point or main function 
 that triggers the creation of documentation.

