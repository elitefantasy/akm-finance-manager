from pathlib import Path

# Files and folders to ignore
IGNORE = {
    # Version control
    ".git",
    ".github",

    # Python
    ".venv",
    "__pycache__",
    "*.pyc",

    # Kivy
    ".kivy",

    # IDE / OS
    ".vscode",
    ".idea",
    ".agents",
    "desktop.ini",
    ".DS_Store",

    # Generated folders
    "bin",
    "build",
    "logs",
    "backups",
    "exports",

    # Files not useful for source overview
    ".gitkeep",
    ".gitignore",
    "README.md",
    "tree.py",
}


def should_ignore(path: Path) -> bool:
    if path.name in IGNORE:
        return True

    if path.suffix == ".pyc":
        return True

    return False


def print_tree(folder: Path, prefix=""):
    items = sorted(
        [p for p in folder.iterdir() if not should_ignore(p)],
        key=lambda p: (p.is_file(), p.name.lower())
    )

    for index, item in enumerate(items):
        last = index == len(items) - 1
        connector = "└── " if last else "├── "

        print(prefix + connector + item.name)

        if item.is_dir():
            extension = "    " if last else "│   "
            print_tree(item, prefix + extension)


if __name__ == "__main__":
    root = Path(".")
    print(root.resolve().name)
    print_tree(root)