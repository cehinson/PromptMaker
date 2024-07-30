# PromptMaker

## Description

PromptMaker is a Python tool that generates structured prompts from project files. It's designed to analyze codebases, providing a comprehensive overview of the project structure and file contents. This tool is particularly useful for developers, code reviewers, and AI assistants working with large codebases.

## Features

- Recursively scans project directories
- Filters files based on include/ignore patterns
- Detects file types and programming languages
- Generates a tree-like structure of the project (optional)
- Provides file contents or summaries based on file size
- Customizable base and task instructions

## Requirements

- Python 3.6+
- `tree` command-line utility (optional, for directory structure visualization)
- `ctags` command-line utility (optional, for large file summaries)

## Installation

You can install PromptMaker using pip:

```
pip install promptmaker
```

Or, for the latest development version, you can install directly from the GitHub repository:

```
pip install git+https://github.com/yourusername/PromptMaker.git
```

## Usage

After installation, you can run PromptMaker from the command line:

```
promptmaker [options] [project_directory]
```

### Options

- `project_directory`: Path to the project directory (default: current directory)
- `--include`: Glob patterns to include (takes precedence over ignore)
- `--ignore`: Glob patterns to ignore
- `--base-instructions`: Custom base instructions for the prompt
- `--task-instructions`: Custom task instructions for the prompt
- `--no-tree`: Disable tree command output
- `--output`: Specify an output file (default: stdout)
- `--max-file-size`: Maximum file size in bytes before using ctags summary (default: 10000)

### Example

```
promptmaker ~/my_project --include "*.py" "*.js" --ignore "tests/*" --output analysis.txt
```

This command will analyze all Python and JavaScript files in the `~/my_project` directory, excluding the `tests` directory, and save the output to `analysis.txt`.

## Output

The script generates a structured prompt containing:

1. Base instructions
2. Project structure (if tree is enabled)
3. File contents or summaries for each included file
4. Task instructions

## Customization

You can customize the base and task instructions to tailor the output for specific use cases. For example:

```
promptmaker . --base-instructions "Analyze this codebase for security vulnerabilities" --task-instructions "Provide a detailed report on potential security issues found in the code"
```

## Development

To set up the project for development:

1. Clone the repository:
   ```
   git clone https://github.com/cehinson/PromptMaker.git
   cd PromptMaker
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the package in editable mode:
   ```
   pip install -e .
   ```

Now you can make changes to the code and test them immediately.

## Project Structure

```
PromptMaker/
├── README.md
├── promptmaker/
│   ├── __init__.py
│   └── main.py
└── setup.py
```
