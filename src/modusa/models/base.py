#!/usr/bin/env python3


from abc import ABC, abstractmethod

class ModusaSignal(ABC):
	"""
	Base class for any signal in the modusa framework.
	
	Note
	----
	- Intended to be subclassed.
	"""
	
	#--------Meta Information----------
	_name = "Modusa Signal"
	_nickname = "MS" # This is to be used in repr/str methods
	_description = "Base class for any signal types in the Modusa framework."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-06-23"
	#----------------------------------
	
	def __init__(self):
		pass
		

class ModusaSignalAxis(ABC):
	"""
	Base class for any modusa signal axis in the modusa framework.
	
	Note
	----
	- Intended to be subclassed.
	"""
	
	#--------Meta Information----------
	_name = "Modusa Signal Axis"
	_nickname = "MSAx" # This is to be used in repr/str methods
	_description = "Base class for any modusa signal axis in the modusa framework."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-25"
	#----------------------------------
	
	def __init__(self):
		pass
	
class ModusaSignalData(ABC):
	"""
	Base class for any modusa signal data in the modusa framework.
	
	Note
	----
	- Intended to be subclassed.
	"""
	
	#--------Meta Information----------
	_name = "Modusa Signal Data"
	_nickname = "MSData" # This is to be used in repr/str methods
	_description = "Base class for any modusa signal data in the modusa framework."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-27"
	#----------------------------------
	
	def __init__(self):
		pass

	