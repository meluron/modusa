#!/usr/bin/env python3


from .generate_template import TemplateGenerator
from .generate_docs_source import generate_docs_source
from .list_plugins import list_plugins
from . import list_authors

import argparse
import sys

def main():
	try:
		parser = argparse.ArgumentParser(
			prog="modusa-dev",
			description="Modusa CLI Tools"
		)
		subparsers = parser.add_subparsers(dest="group", required=True)
		
		# --- CREATE group ---
		create_parser = subparsers.add_parser("create", help="Create new Modusa components")
		create_subparsers = create_parser.add_subparsers(dest="what", required=True)
		
		create_subparsers.add_parser("tool", help="Create a new tool class").set_defaults(func=lambda:TemplateGenerator.create_template("tool"))
		create_subparsers.add_parser("plugin", help="Create a new plugin class").set_defaults(func=lambda:TemplateGenerator.create_template("plugin"))
		create_subparsers.add_parser("model", help="Create a new model class").set_defaults(func=lambda:TemplateGenerator.create_template("model"))
		create_subparsers.add_parser("generator", help="Create a new signal generator class").set_defaults(func=lambda:TemplateGenerator.create_template("generator"))
		create_subparsers.add_parser("io", help="Create a new IO class").set_defaults(func=lambda:TemplateGenerator.create_template("io"))
		create_subparsers.add_parser("docs", help="Generate the docs").set_defaults(func=lambda:generate_docs_source())
		
		# --- LIST group ---
		list_parser = subparsers.add_parser("list", help="List information about Modusa components")
		list_subparsers = list_parser.add_subparsers(dest="what", required=True)
		
		list_subparsers.add_parser("plugins", help="List available plugins").set_defaults(func=list_plugins)
		list_subparsers.add_parser("authors", help="List plugin authors").set_defaults(func=list_authors)
		
		# --- Parse and execute ---
		args = parser.parse_args()
		args.func()
		
	except KeyboardInterrupt:
		print("\n❌ Aborted by user.")
		sys.exit(1)
		