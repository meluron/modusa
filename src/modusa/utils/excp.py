#!/usr/bin/env python3


#----------------------------------------
# Base class errors
#----------------------------------------
class ModusaBaseError(Exception):
	"""
	Ultimate base class for any kind of custom errors.
	"""
	pass

class TypeError(ModusaBaseError):
	pass
	
class InputError(ModusaBaseError):
	"""
	Any Input type error.
	"""

class InputTypeError(ModusaBaseError):
	"""
	Any Input type error.
	"""

class InputValueError(ModusaBaseError):
	"""
	Any Input type error.
	"""
	
class OperationNotPossibleError(ModusaBaseError):
	"""
	Any errors if there is an operations
	failure.
	"""
	
class ImmutableAttributeError(ModusaBaseError):
	"""Raised when attempting to modify an immutable attribute."""
	pass
	
class FileNotFoundError(ModusaBaseError):
	"""Raised when file does not exist."""
	pass
	
class PluginInputError(ModusaBaseError):
	pass

class PluginOutputError(ModusaBaseError):
	pass