# 📃 AutoDocGen

AutoDocGen is a Python-based tool that automatically generates docstrings and project documentation using AI. It includes a CLI, VS Code extension, and a full-featured GUI. Ideal for keeping your code well-documented with minimal effort.

![AutoDocGen Demo]()

---

## ✨ Features

- 🧠 **AI-generated docstrings** using function names and code context
- 🖼️ **Tkinter GUI** for visual review and injection
- 🖥️ **VS Code extension** for inline docstring editing
- 🧰 **Markdown / HTML / PDF / README** generation
- 📁 Ignore folders (e.g. `__pycache__`, `build`, `venv`)
- 🔄 GitHub Actions integration for CI/CD

---

## 🚀 Getting Started

### 🔧 Installation

```bash
git clone https://github.com/chirag-agrawal24/autodocgen.git
pip install -e .
```
📄Optional (only if using AI features): Create a .env file in the project root with your [Groq API key](https://console.groq.com/keys)

```
GROQ_API_KEY=your_groq_api_key_here
```
> Requires Python 3.10 or above


---

## 🧪 Usage

### 🖥️ Command-Line Interface (CLI)

To view all available commands and options:

```bash
autodocgen --help
```

Example: Generate documentation for your project

```bash
autodocgen run --path . --output ./autodocs_output --ignore __pycache__ venv --use-ai
```

**Common Options:**

* `--path`: Path to your Python project directory.
* `--output`: Directory where generated documentation will be saved.
* `--ignore`: Space-separated folders to exclude (e.g., `__pycache__`, `venv`).
* `--use-ai`: Enable AI-based docstring generation.
* `--format`: Output format: `html`, `markdown`, or `pdf`.
* `--readme`: Generate a README file based on project content.

> 💡 Run `autodocgen --help` to explore **all available options** and features.

---

### 🧠 Graphical User Interface (GUI)

Launch the GUI:

```bash
python -m autodocgen gui
# OR
autodocgen gui
```

### 🖼 GUI Requirements

AutoDocGen's GUI uses `tkinter`, which is included with most standard Python installations.
However, on **Linux**, you may need to install it manually:

#### 🔧 For Debian/Ubuntu:

```bash
sudo apt-get install python3-tk
```

#### 🔧 For Arch Linux:

```bash
sudo pacman -S tk
```

#### ✅ Windows & macOS:

No additional steps — `tkinter` usually comes pre-installed with Python.If it's missing, install Python from python.org with the "tcl/tk" option checked.

---


**Features:**

* 📁 Browse and select project/output folders.
* 🔍 Review existing and AI-generated docstrings.
* ❌ Reject or 💾 inject suggestions.
* 📝 Export HTML, Markdown, PDF docs.
* 📘 AI-assisted README editor with preview.

---

## 🧩 VS Code Extension

### 💻 Local Development

To build the extension locally:

```bash
cd vscode-extension
npm install
npm run compile
```

To package it into a `.vsix` file:

```bash
vsce package
```

### 🧩 Installing the Extension

You can install the VS Code extension in two ways:

#### 🔹 Option 1: Download from GitHub Releases

1. Go to the [Releases](https://github.com/chirag-agrawal24/autodocgen/releases) section.
2. Download the latest `.vsix` file.

Install it using:

```bash
code --install-extension autodocgen-<version>.vsix
```

> Replace `<version>` with the version number in the filename.

#### 🔹 Option 2: Build and install locally (as shown above)

This lets you use AutoDocGen directly in VS Code to generate and manage docstrings interactively.

---


## 🔄 GitHub Actions

Includes two workflows:

* `autodocgen.yml`: Auto-generates documentation on code push or PR
* `release.yml`: Builds Python package and VS Code extension on tag push (e.g. `v1.2.3`)

---

## 📁 Project Structure

```
autodocgen/
├── __init__.py
├── __main__.py
├── cli.py
├── gui_app.py
├── runner.py
├── parser.py
├── generator.py
├── ai_docstring_generator.py
├── inject_docstrings.py
├── logger.py
vscode-extension/
tests/
requirements.txt
setup.py
```

### `autodocgen` Package

The `autodocgen` package contains the core functionality of the AutoDocGen tool. It includes the following modules:

* `ai_docstring_generator.py`: Uses the Groq API to generate documentation for Python files and projects.
* `cli.py`: Provides the command-line interface for the AutoDocGen tool.
* `generator.py`: Generates documentation for Python projects, including PDF export and README generation.
* `gui_app.py`: Provides the graphical user interface for the AutoDocGen tool.
* `inject_docstrings.py`: Injects AI-generated docstrings into Python code.
* `logger.py`: Handles logging for the AutoDocGen tool.
* `parser.py`: Parses Python files and generates abstract syntax trees (ASTs).
* `runner.py`: Runs the AutoDocGen tool and generates documentation.
* `setup.py` : For building AutoDocGen package and installing its dependencies
---