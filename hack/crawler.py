from cmd import send

def list_dir(path):
    """Run `ls -F` on a path and return (dirs, files)."""
    output = send(f"ls -F {path}" if path else "ls -F")
    dirs, files = [], []

    for line in output.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.endswith('/'):
            dirs.append(line[:-1])
        elif line.endswith(('*', '@', '=', '|')):
            files.append(line[:-1])
        else:
            files.append(line)

    return dirs, files


def crawl(path="", max_depth=None, _depth=0, _visited=None):
    """
    Recursively map directories starting at `path`.
    Returns a nested dict: {dir_name: {...}, '__files__': [...]}
    """
    if _visited is None:
        _visited = set()

    abs_marker = path or "."
    if abs_marker in _visited:
        return {"__files__": [], "__error__": "cycle detected"}
    _visited.add(abs_marker)

    if max_depth is not None and _depth > max_depth:
        return {"__files__": [], "__truncated__": True}

    tree = {"__files__": []}

    try:
        dirs, files = list_dir(path)
    except Exception as e:
        return {"__files__": [], "__error__": str(e)}

    tree["__files__"] = files

    for d in dirs:
        subpath = f"{path}/{d}" if path else d
        tree[d] = crawl(subpath, max_depth, _depth + 1, _visited)

    return tree


def tree_lines(tree, name=".", indent=""):
    """Build the pretty-print tree as a list of lines (instead of printing)."""
    lines = [f"{indent}{name}/"]
    child_indent = indent + "  "

    for key, val in tree.items():
        if key == "__files__":
            for f in val:
                lines.append(f"{child_indent}{f}")
        elif key in ("__error__", "__truncated__"):
            lines.append(f"{child_indent}[{key}: {val}]")
        else:
            lines.extend(tree_lines(val, key, child_indent))

    return lines


def flatten(tree, base=""):
    """Yield every file/dir as a full path string."""
    for f in tree.get("__files__", []):
        yield f"{base}/{f}" if base else f
    for key, val in tree.items():
        if key not in ("__files__", "__error__", "__truncated__"):
            subbase = f"{base}/{key}" if base else key
            yield subbase  # the directory itself
            yield from flatten(val, subbase)


def write_tree_file(tree, out_path="tree.txt", root_name="."):
    lines = tree_lines(tree, root_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Tree written to {out_path}")


def write_paths_file(tree, out_path="paths.txt"):
    with open(out_path, "w", encoding="utf-8") as f:
        for p in flatten(tree):
            f.write(p + "\n")
    print(f"Paths written to {out_path}")


if __name__ == "__main__":
    result = crawl(path="", max_depth=20)

    write_tree_file(result, "tree.txt")
    write_paths_file(result, "paths.txt")