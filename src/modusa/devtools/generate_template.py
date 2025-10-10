#!/usr/bin/env python3

from datetime import date
from pathlib import Path
import questionary
import sys

ROOT_DIR = Path(__file__).parents[3].resolve()
SRC_CODE_DIR = ROOT_DIR / "src/modusa"
TESTS_DIR = ROOT_DIR / "tests"
TEMPLATES_DIR = ROOT_DIR / "src/modusa/devtools/templates"

PLUGIN_INFO = {
	"template_fp": TEMPLATES_DIR / "plugin.py",
	"test_template_fp": TEMPLATES_DIR / "test.py",
	"template_dump_dp": SRC_CODE_DIR / "plugins",
	"test_template_dump_dp": TESTS_DIR / "test_plugins"
}
IO_INFO = {
	"template_fp": TEMPLATES_DIR / "io.py",
	"test_template_fp": TEMPLATES_DIR / "test.py",
	"template_dump_dp": SRC_CODE_DIR / "io",
	"test_template_dump_dp": TESTS_DIR / "test_io"
}
GENERATOR_INFO = {
	"template_fp": TEMPLATES_DIR / "generator.py",
	"test_template_fp": TEMPLATES_DIR / "test.py",
	"template_dump_dp": SRC_CODE_DIR / "generators",
	"test_template_dump_dp": TESTS_DIR / "test_generators"
}
MODEL_INFO = {
	"template_fp": TEMPLATES_DIR / "model.py",
	"test_template_fp": TEMPLATES_DIR / "test.py",
	"template_dump_dp": SRC_CODE_DIR / "models",
	"test_template_dump_dp": TESTS_DIR / "test_models"
}
TOOL_INFO = {
	"template_fp": TEMPLATES_DIR / "tool.py",
	"test_template_fp": TEMPLATES_DIR / "test.py",
	"template_dump_dp": SRC_CODE_DIR / "tools",
	"test_template_dump_dp": TESTS_DIR / "test_tools"
}


class TemplateGenerator():
	"""
	Generates template for `plugin`, `engine`, `signal`, `generator` along with its corresponding `test` file
	in the `tests` directory.
	"""
	
	
	@staticmethod
	def get_path_info(for_what: str):
		if for_what == "plugin": return PLUGIN_INFO
		if for_what == "io": return IO_INFO
		if for_what == "model": return MODEL_INFO
		if for_what == "tool": return TOOL_INFO
		if for_what == "generator": return GENERATOR_INFO
	
	@staticmethod
	def ask_questions(for_what: str, path_info: dict) -> dict:
		"""Asks question about the template to be generated."""
		print("----------------------")
		print(for_what.upper())
		print("----------------------")
		module_name = questionary.text("Module name (snake_case): ").ask()
		
		if module_name is None:
			sys.exit(1)
			
		if not module_name.endswith(".py"): # Adding extension
			module_name = module_name + ".py"
		# Checking if the module name already exists in the dump directory
		if (path_info["template_dump_dp"] / module_name).exists():
			print(f"⚠️ File already exists, choose another name.")
			sys.exit(1)
		
		class_name = questionary.text(f"Class name (CamelCase): ").ask()
		if class_name is None:
			sys.exit(1)
			
		author_name = questionary.text("Author name: ").ask()
		if author_name is None:
			sys.exit(1)
		
		author_email = questionary.text("Author email: ").ask()
		if author_email is None:
			sys.exit(1)
		
		answers = {"for_what": for_what, "module_name": module_name, "class_name": class_name, "author_name": author_name, "author_email": author_email, "date_created": date.today()}
			
		return answers
	
	@staticmethod
	def load_template_file(template_fp: Path) -> str:
		"""Loads template file."""
		if not template_fp.exists():
			print(f"❌ Template not found: {template_fp}")
			sys.exit(1)
		
		template_code = template_fp.read_text()
		
		return template_code
	
	@staticmethod
	def fill_placeholders(template_code: str, placehoders_dict: dict) -> str:
		"""Fills placeholder in the template with the user input from CLI."""
		template_code = template_code.format(**placehoders_dict)  # Fill placeholders
		return template_code
	
	@staticmethod
	def save_file(content: str, output_path: Path) -> None:
		"""Saves file in the correct directory with the right tempalate content."""
		output_path.parent.mkdir(parents=True, exist_ok=True)
		output_path.write_text(content)
		
		# Generating a corresponding test file too
		what_for = output_path.parent.name # plugins, generators, ...
		module_name = output_path.name # this.py
	
	
	@staticmethod
	def create_template(for_what: str) -> None:
		
		# Load correct path location info for the templates and where to dump the files
		path_info: dict = TemplateGenerator.get_path_info(for_what)
		
		# Ask basic questions to create the template for `plugin`, `generator`, ...
		answers: dict = TemplateGenerator.ask_questions(for_what, path_info)
		
		# Load the correct template file and test file
		template_code: str = TemplateGenerator.load_template_file(template_fp=path_info['template_fp'])
		test_code: str = TemplateGenerator.load_template_file(template_fp=path_info['test_template_fp'])
		
		# Update the dynamic values based on the answers
		template_code: str = TemplateGenerator.fill_placeholders(template_code, answers)
		test_code: str = TemplateGenerator.fill_placeholders(test_code, answers)
		
		# Save it to a file and put it in the correct folder
		TemplateGenerator.save_file(content=template_code, output_path=path_info['template_dump_dp'] / answers['module_name'])
		TemplateGenerator.save_file(content=test_code, output_path=path_info['test_template_dump_dp'] / f"test_{answers['module_name']}")
		
		print(f"✅ {for_what}:", "open " + str(path_info['template_dump_dp'] / answers['module_name']))
		print(f"✅ test:", "open " + str(path_info['test_template_dump_dp'] / f"test_{answers['module_name']}"))