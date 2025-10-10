#!/usr/bin/env python3

from modusa import excp
from functools import wraps
from typing import Any, Callable, Type
from inspect import signature, Parameter
from typing import get_origin, get_args, Union
import types


#----------------------------------------------------
# Safety check for plugin (apply method)
# Check if the input type, output type is allowed,
# Also logs plugin usage.
#----------------------------------------------------
def plugin_safety_check(
	validate_plugin_input: bool = True,
	validate_plugin_output: bool = True,
	track_plugin_usage: bool = True
):
	def decorator(func: Callable) -> Callable:
		@wraps(func)
		def wrapper(self, signal: Any, *args, **kwargs):
			
			if validate_plugin_input:
				if not hasattr(self, 'allowed_input_signal_types'):
					raise excp.AttributeNotFoundError(f"{self.__class__.__name__} must define `allowed_input_signal_types`.")
				
				if type(signal) not in self.allowed_input_signal_types:
					raise excp.PluginInputError(f"{self.__class__.__name__} must take input signal of type {self.allowed_input_signal_types} but got {type(signal)}")
			
			if track_plugin_usage:
				if not hasattr(signal, '_plugin_chain'):
					raise excp.AttributeNotFoundError(f"Signal of type {type(signal).__name__} must have a `_plugin_chain` attribute for plugin tracking.")
					
				if not isinstance(signal._plugin_chain, list):
					raise excp.TypeError(f"`_plugin_chain` must be a list, but got {type(signal._plugin_chain)}")
					
				signal._plugin_chain.append(self.__class__.__name__)
			
			result = func(self, signal, *args, **kwargs)
			
			if validate_plugin_output:
				if not hasattr(self, 'allowed_output_signal_types'):
					raise excp.AttributeNotFoundError(f"{self.__class__.__name__} must define `allowed_output_signal_types`.")
				if type(result) not in self.allowed_output_signal_types:
					raise excp.PluginInputError(f"{self.__class__.__name__} must return output of type {self.allowed_output_signal_types} but returned {type(result)}")
			return result
	
		return wrapper
	return decorator


#----------------------------------------------------
# Safety check for generators (generate method)
# Check if the ouput type is allowed.
#----------------------------------------------------
def generator_safety_check():
	"""
	We assume that the first argument is self, so that we can actually extract properties to
	validate.
	"""
	def decorator(func: Callable) -> Callable:
		@wraps(func)
		def wrapper(self, *args, **kwargs):
			result = func(self, *args, **kwargs)
			
			if not hasattr(self, 'allowed_output_signal_types'):
				raise excp.AttributeNotFoundError(
					f"{self.__class__.__name__} must define `allowed_output_signal_types`."
				)
			if type(result) not in self.allowed_output_signal_types:
				raise excp.PluginInputError(
					f"{self.__class__.__name__} must return output of type {self.allowed_output_signal_types}, "
					f"but returned {type(result)}"
				)
				
			return result
		return wrapper
	return decorator


#----------------------------------------------------
# Validation for args type
# When this decorator is added to a function, it
# automatically checks all the arguments with their
# expected types. (self, forward type references are
# ignored)
#----------------------------------------------------

def validate_arg(arg_name: str, value: Any, expected_type: Any) -> None:
	"""
	Checks if `value_type` matches `expected_type`.
	Raises TypeError if not.
	"""
	import types
	from typing import get_origin, get_args, Union
	
	origin = get_origin(expected_type)
	
	# Handle Union (e.g. int | None)
	if origin in (Union, types.UnionType):
		union_args = get_args(expected_type)
		for typ in union_args:
			typ_origin = get_origin(typ) or typ
			if isinstance(value, typ_origin):
				return
		
		# ❌ If none match
		expected_names = ", ".join(
			get_origin(t).__name__ if get_origin(t) else t.__name__ for t in union_args
		)
		raise excp.InputTypeError(
			f"Argument '{arg_name}' must be one of ({expected_names}), got {type(value).__name__}"
		)
	
	# Handle generic types like list[float], tuple[int, str]
	elif origin is not None:
		if not isinstance(value, origin):
			raise excp.InputTypeError(
				f"Argument '{arg_name}' must be of type {origin.__name__}, got {type(value).__name__}"
			)
		return
		
	# ✅ Handle plain types
	elif isinstance(expected_type, type):
		if not isinstance(value, expected_type):
			raise excp.InputTypeError(
				f"Argument '{arg_name}' must be of type {expected_type.__name__}, got {type(value).__name__}"
			)
		return
	# ❌ Unsupported type structure
	else:
		raise excp.InputTypeError(f"Unsupported annotation for '{arg_name}': {expected_type}")

def validate_args_type() -> Callable:
	def decorator(func: Callable) -> Callable:
		@wraps(func)
		def wrapper(*args, **kwargs):
			sig = signature(func)
			bound = sig.bind(*args, **kwargs)
			bound.apply_defaults()
			
			for arg_name, value in bound.arguments.items():
				param = sig.parameters[arg_name]
				expected_type = param.annotation
				
				# Skip unannotated or special args
				if expected_type is Parameter.empty or arg_name in ("self", "cls") or isinstance(expected_type, str):
					continue
				
				validate_arg(arg_name, value, expected_type)  # <- this is assumed to be defined elsewhere
				
			return func(*args, **kwargs)
		return wrapper
	return decorator

#-----------------------------------
# Making a property immutable
# and raising custom error message
# during attempt to modify the values
#-----------------------------------
def immutable_property(error_msg: str):
	"""
	Returns a read-only property. Raises an error with a custom message on mutation.
	"""
	def decorator(getter):
		name = getter.__name__
		private_name = f"_{name}"
		
		def setter(self, value):
			raise excp.ImmutableAttributeError(error_msg)
			
		return property(getter, setter)
	
	return decorator