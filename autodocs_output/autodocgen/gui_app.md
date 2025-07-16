# autodocgen/gui_app.py

> AI summary failed.


---


## Class: `AutoDocGUI`

No class docstring available.


### Method: `__init__`
- **Arguments**: ['self', 'root']
- **Returns**: None

Initializes the instance with the root window.

 :param self: The instance itself
 :param root: The root window of the application

### Method: `setup_ui`
- **Arguments**: ['self']
- **Returns**: None

Sets up the user interface for the application.

 Initializes and configures the UI components.

 Args:
     self: A reference to the current instance of the class.

 Returns:
     None

### Method: `browse_project`
- **Arguments**: ['self']
- **Returns**: None

Opens a file dialog for the user to select a project directory and navigates to it.

### Method: `browse_output`
- **Arguments**: ['self']
- **Returns**: None

Opens a file dialog for browsing and selecting output files or directories. 

No arguments other than self are required. 

Returns None

### Method: `add_ignore_folder`
- **Arguments**: ['self']
- **Returns**: None

Adds a folder to the ignore list, excluding it from documentation generation. 
No arguments are taken besides the implicit class reference.

### Method: `clear_ignore_folders`
- **Arguments**: ['self']
- **Returns**: None

Clears the list of folders to be ignored during documentation generation. 

No arguments are required. 

Returns: None

### Method: `generate_docstrings`
- **Arguments**: ['self']
- **Returns**: None

Generate docstrings for the current object.

### or in Google style:
Generates docstrings for the current object. 

### or in NumPy style:
Generate docstrings for the current object
         Parameters
         ----------
         self : 
             The object instance. 

Here I provided 3 types it can be written. I assume you need the NumPy style.

 
Parameters
----------
self : 
    The object instance.

### Method: `on_tree_select`
- **Arguments**: ['self', 'event']
- **Returns**: None

Handles the selection of a tree item.

 
Parameters
self: A reference to the instance of the class
event: The event triggered by the tree selection 

Returns
None

### Method: `reject_current_docstring`
- **Arguments**: ['self']
- **Returns**: None

Rejects the current docstring, presumably removing or invalidating it. 
No parameters are required beyond the instance reference.

### Method: `save_final_docstrings`
- **Arguments**: ['self']
- **Returns**: None

Saves the final docstrings to a file, utilizing AI-powered generation if necessary, 
and exports the documentation in various formats including PDF and README.

### Method: `generate_docs`
- **Arguments**: ['self', 'fmt']
- **Returns**: None

Generate documentation for the given format.

### Parameters
* self: The instance of the class this method belongs to.
* fmt: The format of the documentation to be generated.

### Returns
None

### Method: `generate_pdf`
- **Arguments**: ['self']
- **Returns**: None

Generate a PDF document based on the parsed documentation.

No arguments are required beyond the instance reference.

Returns: None 

or 

Generate a PDF document based on the parsed documentation.

No arguments are required.

Returns: None 

or

### generate_pdf 
 Generate a PDF document based on the parsed documentation. 

### Parameters
 None 

### Returns 
 None

### Method: `generate_readme`
- **Arguments**: ['self']
- **Returns**: None

Generate a README file for the project based on parsed documentation.




---


## Function: `launch`
- **Arguments**: []
- **Returns**: None

Launch the documentation generation process. 
No arguments are required for this function. 
It is assumed to be part of a larger documentation generation application.

