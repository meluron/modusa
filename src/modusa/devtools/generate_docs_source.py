#!/usr/bin/env python3

import inspect
import importlib
import pkgutil
from pathlib import Path
from collections import defaultdict

# === Configuration ===
BASE_MODULES = [
    'modusa.tools',
#   'modusa.models',
#   'modusa.generators',
#   'modusa.plugins',
]
OUTPUT_DIRS = [
    Path('docs/source/tools'),
#   Path('docs/source/models'),
#   Path('docs/source/generators'),
#   Path('docs/source/plugins'),
]

# Ensure output directories exist
for output_dir in OUTPUT_DIRS:
    output_dir.mkdir(parents=True, exist_ok=True)

# === Utils ===
def get_classes_grouped_by_module(base_module):
    """
    Returns a dictionary: { module_path: [class_name, ...] }
    """
    found = defaultdict(list)
    module = importlib.import_module(base_module)

    for _, modname, _ in pkgutil.walk_packages(module.__path__, base_module + "."):
        try:
            submodule = importlib.import_module(modname)
            for name, obj in inspect.getmembers(submodule, inspect.isclass):
                if obj.__module__ == modname:
                    found[modname].append(name)
        except Exception as e:
            print(f"⚠️ Skipping {modname} due to import error: {e}")
    return found

def write_module_rst_file(module_path, class_names, output_dir):
    """
    Writes a .rst file for a module, documenting all its classes.
    Filename is based on the module, but title is the first class (Modusa* gets priority).
    """
    filename = output_dir / f"{module_path.split('.')[-1]}.rst"

    # Prioritize 'Modusa*' classes first, then alphabetical
    sorted_classes = sorted(class_names, key=lambda x: (not x.startswith("Modusa"), x.lower()))
    title = sorted_classes[0] if sorted_classes else module_path.split('.')[-1]

    with open(filename, 'w') as f:
        f.write(f"{title}\n{'=' * len(title)}\n\n")
        for class_name in sorted_classes:
            f.write(f".. autoclass:: {module_path}.{class_name}\n")
            f.write("   :members:\n")
            f.write("   :undoc-members:\n")
            f.write("   :show-inheritance:\n\n")
    
    return filename.name

def write_index_rst_file(tools_by_module, output_dir, section_name="Tools"):
    """
    Writes index.rst in the given output_dir with 'base' on top, then other files alphabetically.
    """
    index_file = output_dir / "index.rst"
    with open(index_file, "w") as f:
        f.write(f"{section_name}\n{'=' * len(section_name)}\n\n")
        f.write(".. toctree::\n   :maxdepth: 1\n\n")

        filenames = [module_path.split('.')[-1] for module_path in tools_by_module]
        sorted_filenames = sorted(filenames, key=lambda x: (x != "base", x.lower()))

        for name in sorted_filenames:
            f.write(f"   {name}\n")

# === Main Script ===
def generate_docs_source():
    for base_module, output_dir in zip(BASE_MODULES, OUTPUT_DIRS):
        module_class_map = get_classes_grouped_by_module(base_module)
    
        for module_path, class_list in module_class_map.items():
            write_module_rst_file(module_path, class_list, output_dir)
    
        section_name = base_module.split('.')[-1].capitalize()
    
        write_index_rst_file(module_class_map, output_dir, section_name=section_name)
        print(f"✅ Documentation generated for {base_module} in {output_dir}")
