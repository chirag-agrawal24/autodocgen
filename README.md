# 📚 AutoDocGen

AutoDocGen is a powerful Python-based tool that uses AI to automatically generate docstrings and full project documentation. It supports both command-line and graphical interfaces, as well as a VS Code extension, making it a complete solution for maintaining professional-grade documentation with minimal effort.

<img width="1912" height="1013" alt="Screenshot 2025-07-16 195446" src="https://github.com/user-attachments/assets/3f3256b8-b3fb-43c8-ac0b-3af4108e4d49" />

### AutoDocGen Markdown Editor
<img width="1919" height="1010" alt="Screenshot 2025-07-16 195624" src="https://github.com/user-attachments/assets/5db2e5c1-dce3-441e-8103-9b639e2b1836" />



---

## ✨ Features

* 🧠 AI-generated docstrings from function signatures and code context
* 🖼️ Full-featured GUI using `tkinter`
* 🧩 VS Code extension for inline documentation
* 📄 Exports documentation to **Markdown**, **HTML**, **PDF**, and **README.md**
* 📁 Folder ignore rules (e.g. `__pycache__`, `venv`, `.git`)
* 🔁 GitHub Actions integration for continuous documentation updates

---

## 🚀 Getting Started

### 🔧 Installation

```bash
git clone https://github.com/chirag-agrawal24/autodocgen.git
pip install -e .
```

> ✅ Requires Python 3.10 or above

### 🔐 Optional: Add Groq API Key

If you want to use AI-based docstring generation, create a `.env` file in the root directory:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

You can obtain your key from [Groq Console](https://console.groq.com/keys).

---

## 🧪 Usage

### 📟 Command-Line Interface (CLI)

Show help menu:

```bash
autodocgen --help
```

Example command:

```bash
autodocgen run --path . --output ./autodocs_output --ignore __pycache__ venv --use-ai
```

**Popular Options:**

* `--path`: Path to project root
* `--output`: Directory to save docs
* `--ignore`: Space-separated folders to exclude
* `--use-ai`: Enable AI docstrings
* `--format`: Output format (html, markdown, pdf)
* `--readme`: Generate README.md based on project

💡 Run `autodocgen --help` to see **all options**.

---

### 🧠 Graphical User Interface (GUI)

Launch GUI:

```bash
python -m autodocgen gui
# OR
autodocgen gui
```

**GUI Features:**

* 📂 Browse and select folders
* 🔍 Preview and edit docstrings
* ❌ Reject / 💾 Inject AI suggestions
* 📄 Export to HTML, Markdown, or PDF
* 🧠 README editor powered by AI

### 🖼 tkinter Requirements

Most systems have tkinter pre-installed. If not:

#### On Ubuntu/Debian:

```bash
sudo apt-get install python3-tk
```

#### On Arch:

```bash
sudo pacman -S tk
```

#### On Windows:

Ensure Python is from [python.org](https://www.python.org/downloads/) with "tcl/tk" enabled. The Microsoft Store version lacks tkinter.

To check if tkinter is working:

```bash
python -m tkinter
```

---

## 🧩 VS Code Extension

### 💻 Develop Locally

```bash
cd vscode-extension
npm install
npm run compile
```

To package it:

```bash
vsce package
```

### 🧩 Install the Extension

You can install it in two ways:

#### Option 1: From GitHub Releases

1. Go to the [Releases](https://github.com/chirag-agrawal24/autodocgen/releases)
2. Download `.vsix` file
3. Install via:

```bash
code --install-extension autodocgen-<version>.vsix
```

#### Option 2: Build & Install Locally

Great for testing your edits live in VS Code.

---

## 🔄 GitHub Actions

AutoDocGen comes with two workflows:

* `autodocgen.yml`: Automatically generates and commits updated documentation on push or PR
* `release.yml`: Builds and packages the Python project and VS Code extension when a new tag is pushed

---

## 🗂️ Project Structure

```
autodocgen/
├── __init__.py
├── __main__.py
├── ai_docstring_generator.py
├── cli.py
├── generator.py
├── gui_app.py
├── inject_docstrings.py
├── logger.py
├── parser.py
├── runner.py
vscode-extension/
tests/
requirements.txt
setup.py
```

### `autodocgen` Package Modules

* `ai_docstring_generator.py`: Uses Groq API to generate docstrings
* `cli.py`: CLI handler
* `generator.py`: Handles doc and PDF generation
* `gui_app.py`: GUI interface with folder browser and docstring editor
* `inject_docstrings.py`: Inserts AI-generated docstrings into source files
* `logger.py`: Logging setup
* `parser.py`: AST-based code parser
* `runner.py`: Main execution logic
* `setup.py`: Install script for building and installing dependencies

---

## 🧵 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss your ideas.

---
