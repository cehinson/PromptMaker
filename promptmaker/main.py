#!/usr/bin/env python3
import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path

from tqdm import tqdm


def get_language(file_path):
    extension_to_language = {
        ".py": "python3",
        ".js": "javascript",
        ".html": "html",
        ".css": "css",
        ".java": "java",
        ".c": "c",
        ".cpp": "cpp",
        ".h": "cpp",
        ".sh": "bash",
        ".md": "markdown",
        ".json": "json",
        ".xml": "xml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".sql": "sql",
        ".rb": "ruby",
        ".php": "php",
        ".go": "go",
        ".rs": "rust",
        ".ts": "typescript",
        ".kt": "kotlin",
        ".swift": "swift",
        ".m": "objectivec",
        ".lua": "lua",
    }
    extension = file_path.suffix.lower()
    return extension_to_language.get(extension, "plaintext")


def should_include(file_path, include_patterns, ignore_patterns):
    file_str = str(file_path)

    if include_patterns:
        return any(fnmatch.fnmatch(file_str, pattern) for pattern in include_patterns)

    return not any(fnmatch.fnmatch(file_str, pattern) for pattern in ignore_patterns)


def get_tree_output(project_dir):
    try:
        result = subprocess.run(["tree", project_dir], capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        print(
            "Error: 'tree' command not found. Please install it or add it to your PATH."
        )


def get_ctags_output(file_path):
    try:
        result = subprocess.run(
            [
                "ctags",
                "-x",
                "--fields=+KnS",
                "--output-format=xref",
                "--extras=+q",
                str(file_path),
            ],
            capture_output=True,
            text=True,
        )
        return result.stdout
    except FileNotFoundError:
        print(
            "Error: 'ctags' command not found. Please install it or add it to your PATH."
        )


def get_word_count(text):
    try:
        result = subprocess.run(
            ["wc", "-w"], input=text, text=True, capture_output=True
        )
        return int(result.stdout.strip().split()[0])
    except FileNotFoundError:
        return len(text.split())


def generate_prompt(
    project_dir,
    include_patterns,
    ignore_patterns,
    base_instructions,
    task_instructions,
    use_tree,
    max_file_size,
):
    project_path = Path(project_dir).resolve()

    prompt = f"Base Instructions:\n{base_instructions}\n\n"
    prompt += "Background Information:\n"

    if use_tree:
        tree_output = get_tree_output(project_dir)
        if tree_output:
            prompt += f"Project structure:\n```\n{tree_output}\n```\n\n"

    all_files = list(project_path.rglob("*"))

    included_files = [
        f
        for f in all_files
        if f.is_file()
        and should_include(
            f.relative_to(project_path), include_patterns, ignore_patterns
        )
        and not f.name.startswith(".")
        and not any(part.startswith(".") for part in f.parts)
    ]

    for file_path in tqdm(included_files, desc="Processing files", unit="file"):
        relative_path = file_path.relative_to(project_path)
        language = get_language(file_path)
        file_size = file_path.stat().st_size

        prompt += f"File: {relative_path}\n"

        if file_size > max_file_size:
            ctags_output = get_ctags_output(file_path)
            if ctags_output:
                prompt += f"File size: {file_size} bytes. Showing ctags summary:\n```\n{ctags_output}\n```\n\n"
        else:
            prompt += f"```{language}\n"
            try:
                with open(file_path, "r", encoding="utf-8") as in_file:
                    prompt += in_file.read()
            except UnicodeDecodeError:
                prompt += f"[Unable to read file: {relative_path}]\n"
            prompt += "\n```\n\n"

    prompt += f"\nTask Instructions:\n{task_instructions}\n"

    return prompt


def main():
    parser = argparse.ArgumentParser(
        description="Generate a structured prompt from project files."
    )
    parser.add_argument(
        "project_dir", nargs="?", default=".", help="Path to the project directory"
    )
    parser.add_argument(
        "--include",
        nargs="*",
        default=[],
        help="Glob patterns to include (takes precedence over ignore)",
    )
    parser.add_argument(
        "--ignore",
        nargs="*",
        default=[],
        help="Glob patterns to ignore (used if no include patterns match)",
    )
    parser.add_argument(
        "--base-instructions",
        default="You are an AI assistant tasked with analyzing and working with the provided codebase. If you don't have enough information to complete a task, please admit it.",
        help="Base instructions to prepend",
    )
    parser.add_argument(
        "--task-instructions",
        default="Please analyze the provided code and suggest improvements.",
        help="Task instructions to append",
    )
    parser.add_argument(
        "--no-tree",
        action="store_true",
        help="Disable tree command output (tree is included by default)",
    )
    parser.add_argument("--output", help="Output file (default is stdout)")
    parser.add_argument(
        "--max-file-size",
        type=int,
        default=10000,
        help="Maximum file size in bytes before using ctags summary (default: 10000)",
    )

    args = parser.parse_args()

    use_tree = not args.no_tree
    prompt = generate_prompt(
        args.project_dir,
        args.include,
        args.ignore,
        args.base_instructions,
        args.task_instructions,
        use_tree,
        args.max_file_size,
    )

    word_count = get_word_count(prompt)
    print(f"\nPrompt generated. Word count: {word_count}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out_file:
            out_file.write(prompt)
        print(f"Prompt written to {args.output}")
    else:
        sys.stdout.write(prompt)


if __name__ == "__main__":
    main()
