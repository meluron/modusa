#!/usr/bin/env python3

from abc import ABC, abstractmethod

class ModusaTool(ABC):
	"""
	Base class for all tool: youtube downloader, audio converter, filter.
	
	>>> modusa-dev create io

	.. code-block:: python
		
		# General template of a subclass of ModusaTool
		from modusa.tools.base import ModusaTool

		class MyCustomIOClass(ModusaIO):
			#--------Meta Information----------
			_name = "My Custom Tool"
			_description = "My custom class for Tool."
			_author_name = "Ankit Anand"
			_author_email = "ankit0.anand0@gmail.com"
			_created_at = "2025-07-06"
			#----------------------------------
			
			@staticmethod
			def do_something():
				pass
		
	
	Note
	----
	- This class is intended to be subclassed by any tool built for the modusa framework.
	- In order to create a tool, you can use modusa-dev CLI to generate a template.
	- It is recommended to treat subclasses of ModusaTool as namespaces and define @staticmethods with control parameters, rather than using instance-level __init__ methods.
	"""
	
	#--------Meta Information----------
	_name: str = "Modusa Tool"
	_description: str = "Base class for any tool in the Modusa framework."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-11"
	#----------------------------------