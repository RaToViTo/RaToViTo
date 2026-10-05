import ast
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
PYTHON_DIR = PROJECT_ROOT / "backend"


def get_imports(file_path):
    """Return all absolute import names from a Python file or notebook."""
    imports = set()

    try:
        if file_path.suffix == ".ipynb":
            notebook = json.loads(
                file_path.read_text(encoding="utf-8")
            )

            sources = [
                "".join(cell.get("source", []))
                for cell in notebook.get("cells", [])
                if cell.get("cell_type") == "code"
            ]
        else:
            sources = [
                file_path.read_text(encoding="utf-8")
            ]

        for source in sources:
            try:
                tree = ast.parse(source)
            except SyntaxError:
                continue

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)

    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ):
        pass

    return imports


def get_module_name(file_path):
    """
    Convert:

        backend/isotope_simulation/plot_config.py

    into:

        backend.isotope_simulation.plot_config
    """
    relative = file_path.relative_to(PROJECT_ROOT)

    return ".".join(
        relative.with_suffix("").parts
    )


def build_module_map():
    """Create a map from module name to Python file."""

    modules = {}

    for file in PYTHON_DIR.rglob("*.py"):
        modules[get_module_name(file)] = file

    return modules


def resolve_import(import_name, modules):
    """
    Resolve an import such as:

        backend.isotope_simulation.plot_config

    to:

        backend/isotope_simulation/plot_config.py
    """

    # Exact module match
    if import_name in modules:
        return modules[import_name]

    # Try progressively shorter module names
    parts = import_name.split(".")

    for i in range(len(parts), 0, -1):
        candidate = ".".join(parts[:i])

        if candidate in modules:
            return modules[candidate]

    return None


def main():

    modules = build_module_map()

    py_files = list(PYTHON_DIR.rglob("*.py"))
    notebooks = list(PROJECT_ROOT.rglob("*.ipynb"))

    # ---------------------------------------------------------
    # Collect imports from notebooks
    # ---------------------------------------------------------

    notebook_imports = set()

    for notebook in notebooks:
        notebook_imports.update(
            get_imports(notebook)
        )

    # ---------------------------------------------------------
    # Follow dependencies recursively
    # ---------------------------------------------------------

    used_files = set()

    queue = list(notebook_imports)

    while queue:

        import_name = queue.pop()

        file = resolve_import(
            import_name,
            modules,
        )

        if file is None:
            continue

        if file in used_files:
            continue

        used_files.add(file)

        # Find imports inside this Python file
        dependencies = get_imports(file)

        for dependency in dependencies:

            dependency_file = resolve_import(
                dependency,
                modules,
            )

            if (
                dependency_file is not None
                and dependency_file not in used_files
            ):
                queue.append(dependency)

    # ---------------------------------------------------------
    # Find potentially unused files
    # ---------------------------------------------------------

    unused = []

    scanner_file = Path(__file__).resolve()

    for file in py_files:

        if file.resolve() == scanner_file:
            continue

        if file not in used_files:
            unused.append(file)

    # ---------------------------------------------------------
    # Output
    # ---------------------------------------------------------

    print(
        f"Potentially unused .py files ({len(unused)}):\n"
    )

    for file in sorted(unused):
        print(
            file.relative_to(PROJECT_ROOT)
        )


if __name__ == "__main__":
    main()
