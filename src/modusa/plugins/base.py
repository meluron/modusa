#!/usr/bin/env python3

from modusa.decorators import plugin_safety_check
from abc import ABC, abstractmethod
from typing import Any

class ModusaPlugin(ABC):
	"""
	Base class for any Plugin that follows the modusa framework.
	"""
	
	@property
	@abstractmethod
	def allowed_input_signal_types(self) -> tuple[type, ...]:
		"""
		Define the expected signal types for this plugin.
		
		Note
		----
		- Must be implemented by every `ModusaPlugin` subclass.
		- Clearly states what signal types are accepted in `.apply()`.
		- Return a tuple of accepted signal classes.
		
		Examples
		--------
		.. code-block:: python

			# Single type
			from modusa.signals import Signal1D
			return (Signal1D, )
		
			# Multiple types
			from modusa.signals import Signal1D, Signal2D
			return (Signal1D, Signal2D)
		"""
		pass
		
	@property
	@abstractmethod
	def allowed_output_signal_types(self) -> tuple[type, ...]:
		"""
		Defines the allowed return types from the `.apply()` method.
		
		Note
		----
		- Must be implemented by every `ModusaPlugin` subclass.
		- Clearly declares what return types are valid.
		- Return a tuple of accepted types (usually signal classes).
		
		Examples
		--------
		.. code-block:: python

			# Single type allowed
			from modusa.signals import Signal1D
			return (Signal1D, )
		
			# Multiple types allowed
			from modusa.signals import Signal1D, Signal2D
			return (Signal1D, Signal2D)
		
			# Return type can also be None (e.g., for plot-only plugins)
			from modusa.signals import Signal1D, Signal2D
			return (Signal1D, Signal2D, type(None))
		"""
		pass
		
	@plugin_safety_check()
	@abstractmethod
	def apply(self, signal: Any) -> Any:
		"""
		Defines the main processing logic of the plugin.
		
		Note
		----
		- Must be implemented by every `ModusaPlugin` subclass.
		- It is highly advised to wrap it with `@plugin_safety_check()` to:
			- Validate input and output types.
			- Enforce plugin contracts for safe execution.
		
		Warning
		-------
		- You should not make this method as `classmethod` or `staticmethod`, this will break plugin safety check.
		
		Example
		-------
		.. code-block:: python
			
			@plugin_safety_check()
			def apply(self, signal: "TimeDomainSignal") -> "TimeDomainSignal":
				from modusa.engines import SomeEngine
				new_signal: TimeDomainSignal = SomeEngine.run(signal)
				
				return new_signal
		"""
		pass
		
		
	
		