#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import immutable_property, validate_args_type
from modusa.signals.base import ?
from typing import Self, Any
import numpy as np

class {class_name}():
	"""

	"""
	
	#--------Meta Information----------
	_name = ""
	_nickname = "" # This is to be used in repr/str methods
	_description = ""
	_author_name = "{author_name}"
	_author_email = "{author_email}"
	_created_at = "{date_created}"
	#----------------------------------
	
	@validate_args_type()
	def __init__(self):
		super().__init__() # Instantiating `ModusaSignal` class
	
		self.title = "" # This title will be used as plot title by default
		
	#-----------------------------------
	# Properties
	#-----------------------------------
		
		
	#===================================
		
		
		
		
		
		
	#-----------------------------------
	# Tools
	#-----------------------------------
		
		
	#===================================