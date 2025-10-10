#!/usr/bin/env python3

import inspect
from pathlib import Path

PLUGIN_PATH = Path(__file__).parent.parent / "plugins" # This directory contains all the plugins

def find_plugin_files():
	return [
			path for path in PLUGIN_PATH.rglob("*.py")
			if path.name not in {"__init__.py", "base.py"} # We do not want to show base plugins
		]

def load_plugin_class_from_file(file_path):
	import importlib.util
	from modusa.plugins.base import ModusaPlugin
	
	spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
	module = importlib.util.module_from_spec(spec)
	try:
		spec.loader.exec_module(module)
	except Exception as e:
		print(f"❌ Error loading {file_path}: {e}")
		return []
	
	plugin_classes = []
	for _, obj in inspect.getmembers(module, inspect.isclass):
		if issubclass(obj, ModusaPlugin) and obj is not ModusaPlugin:
			plugin_classes.append(obj)
			
	return plugin_classes

def list_plugins():
	from rich.console import Console
	from rich.table import Table
	from modusa.plugins.base import ModusaPlugin
	
	console = Console()
	table = Table(title="🔌 Available Modusa Plugins")
	
	table.add_column("Plugin", style="bold green")
	table.add_column("Module", style="dim")
	table.add_column("Description", style="white")
	
	all_plugins = []
	
	for file_path in find_plugin_files():
		plugin_classes = load_plugin_class_from_file(file_path)
		for cls in plugin_classes:
			name = cls.__name__
			module = file_path.relative_to(PLUGIN_PATH.parent)
			author = getattr(cls, "author_name", "—")
			email = getattr(cls, "author_email", "—")
			desc = getattr(cls, "description", "—")
			table.add_row(name, str(module), desc)
			table.add_row("")
			all_plugins.append(cls)
			
	console.print(table)

