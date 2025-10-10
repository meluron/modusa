#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import validate_args_type
from modusa.generators.base import ModusaGenerator


class {class_name}(ModusaGenerator):
	"""

	"""
	
	#--------Meta Information----------
	_name = ""
	_description = ""
	_author_name = "{author_name}"
	_author_email = "{author_email}"
	_created_at = "{date_created}"
	#----------------------------------
	
	def __init__(self):
		super().__init__()
	