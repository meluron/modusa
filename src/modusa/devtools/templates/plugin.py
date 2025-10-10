#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import immutable_property, validate_args_type, plugin_safety_check
from modusa.plugins.base import ModusaPlugin


class {class_name}(ModusaPlugin):
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
		
	@immutable_property(error_msg="Mutation not allowed.")
	def allowed_input_signal_types(self) -> tuple[type, ...]:
		return ()
	
	
	@immutable_property(error_msg="Mutation not allowed.")
	def allowed_output_signal_types(self) -> tuple[type, ...]:
		return ()
	
	
	@plugin_safety_check()
	@validate_args_type()
	def apply(self, signal: "") -> "":
		
		# Run the engine here
		
		return 