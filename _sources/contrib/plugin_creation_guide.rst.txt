Plugin Creation Guide
=====================

This guide will walk you through creating a new plugin in the **Modusa** framework.

All plugins must inherit from the base class :class:`modusa.plugins.ModusaPlugin` and implement the required properties and methods to be considered valid and safely executable within the framework.

Plugin Structure
----------------

Each plugin must:
	
1. Define the input and output signal types using the `allowed_input_signal_types` and `allowed_output_signal_types` properties.
2. Implement the main logic inside the `apply()` method.
3. Be decorated with `@plugin_safety_check()` for automatic type validation and safe execution.

Basic Template
^^^^^^^^^^^^^^

Here is a minimal working example of a Modusa plugin:
	
.. code-block:: python

	from modusa.plugins import ModusaPlugin
	from modusa.decorators import plugin_safety_check
	from modusa.signals import Signal1D
	
	class MyPlugin(ModusaPlugin):
		@property
		def allowed_input_signal_types(self):
			# Accept only Signal1D input
			return (Signal1D, )
		
		@property
		def allowed_output_signal_types(self):
			# Return type is also Signal1D
			return (Signal1D, )
		
		@plugin_safety_check()
		def apply(self, signal: Signal1D) -> Signal1D:
			# Plugin processing logic
			y = signal.y * 2
			return Signal1D(y=y, x=signal.x)
		
Explanation of Components
-------------------------

allowed_input_signal_types
^^^^^^^^^^^^^^^^^^^^^^^^^^

This property defines what types of signals your plugin can operate on.

.. code-block:: python

	@property
	def allowed_input_signal_types(self):
		return (Signal1D, Signal2D)

allowed_output_signal_types
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This property defines the types your plugin might return from `apply()`.

.. code-block:: python

	@property
	def allowed_output_signal_types(self):
		return (Signal1D, Signal2D, type(None))  # None for plot-only plugins

apply()
^^^^^^^

This method contains the core logic. You **must** decorate it with `@plugin_safety_check()` to ensure input/output types are automatically checked and errors are raised clearly if the contract is violated.

Do **not** make `apply` a `@staticmethod` or `@classmethod`, as that breaks safety checking.

.. code-block:: python

	@plugin_safety_check()
	def apply(self, signal: Signal1D) -> Signal1D:
		# Do processing here
		return processed_signal

Advanced Notes
--------------

- If your plugin doesn’t return anything (e.g., it only plots), return `None` and include `type(None)` in `allowed_output_signal_types`.
- All signal types should come from `modusa.signals`.

Plugin Discovery
----------------

To be discoverable by the CLI or GUI (if applicable), your plugin class must reside in a Python module that follows the naming conventions required by the framework. Typically, all plugins are placed in a `plugins/` directory or registered via entry points.	