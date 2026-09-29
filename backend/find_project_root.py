# Find the project root by climbing up the path until a known folder exists
def find_project_root(marker_folder="Resources"):

    from pathlib import Path

    path = Path().resolve()
    while not (path / marker_folder).exists():
        if path.parent == path:
            raise RuntimeError("Could not find project root.")
        path = path.parent
    return path
