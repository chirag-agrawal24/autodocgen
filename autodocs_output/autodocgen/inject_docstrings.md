# autodocgen/inject_docstrings.py

> AI summary failed.


---


## Class: `DocstringInjector`

No class docstring available.


### Method: `__init__`
- **Arguments**: ['self', 'file_context', 'force', 'show_diff', 'in_memory_funcs']
- **Returns**: None

Initializes the object with the given context and settings.

  Args:
    file_context: The context of the file being processed.
    force: A flag indicating whether to force certain actions.
    show_diff: A flag indicating whether to show differences.
    in_memory_funcs: A collection of functions stored in memory.

  Note:
    AI-generated docstrings and file descriptions are attempted, 
    falling back to a default description if AI support is unavailable.

### Method: `get_custom_docstring`
- **Arguments**: ['self', 'name']
- **Returns**: None

Get a custom docstring for a given function name.

 Parameters
 ----------
 self : object
     instance of the class
 name : str
     name of the function

 Returns
 -------
 str
     custom docstring for the function

### Method: `visit_FunctionDef`
- **Arguments**: ['self', 'node']
- **Returns**: None

Visits a FunctionDef node and generates a docstring for it using AI if available. 
If AI is unavailable, a placeholder docstring is generated. 
Parameters: 
- node: The FunctionDef node to visit.

### Method: `visit_ClassDef`
- **Arguments**: ['self', 'node']
- **Returns**: None

Visits a ClassDef node and generates a docstring for it. 
Parameters:
- node: The ClassDef node to visit.

### Method: `inject`
- **Arguments**: ['self', 'code']
- **Returns**: None

Injects code into a function and generates a docstring.

 Args:
     code: The code to be injected.

 Returns:
     None 

or using Google style 

Injects code into a function.

 Args:
     code: The code to be injected.

 Returns:
     None

### Method: `show_code_diff`
- **Arguments**: ['self']
- **Returns**: None

Displays the code difference between the current and original versions of a file. 
No arguments are required.




---


## Function: `inject_into_file`
- **Arguments**: ['filepath', 'dest_path', 'force', 'show_diff', 'in_memory_funcs']
- **Returns**: None

Injects a generated docstring into a specified file.

Parameters:
filepath (str): Path to the file to be modified.
dest_path (str): Destination path to write the modified file.
force (bool): Overwrite existing file if True.
show_diff (bool): Display a diff of the changes if True.
in_memory_funcs (dict): Dictionary of functions to process.

Returns:
None 

or use the google style 

Injects a generated docstring into a specified file.

Args:
  filepath: Path to the file to be modified.
  dest_path: Destination path to write the modified file.
  force: Overwrite existing file if True.
  show_diff: Display a diff of the changes if True.
  in_memory_funcs: Dictionary of functions to process.

Returns:
  None

