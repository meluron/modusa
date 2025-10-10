#!/usr/bin/env python3

from modusa import excp
from modusa.decorators import validate_args_type, immutable_property
from modusa.models.base import ModusaSignal
from abc import ABC, abstractmethod
from typing import Any

class ModusaGenerator(ABC):
	"""
	Base class for any type of signal generators for modusa framework.
	
	Note
	----
	- This class is intended to be subclassed by any Generator related tools built for the modusa framework.
	- In order to create a generator tool, you can use modusa-dev CLI to generate an generator template.
	- It is recommended to treat subclasses of ModusaGenerator as namespaces and define @staticmethods with control parameters, rather than using instance-level __init__ methods.
	
	
	"""
	
	#--------Meta Information----------
	_name = ""
	_description = ""
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-04"
	#----------------------------------
	