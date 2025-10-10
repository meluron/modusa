Tool Creation Guide
===================

In Modusa, all core logic **must reside in a separate `ModusaTool` subclass**, not directly inside the plugin.

This ensures:

- Cleaner separation of concerns.
- Reusability of processing logic across plugins, tests, scripts, and CLI tools.
- Easier unit testing (engines don’t depend on plugin infrastructure).
- Plugins remain lightweight and act only as adapters.

Tool Structure
--------------

A **ModusaTool** is a plain Python class or function that performs a specific computation or transformation. It should be completely **decoupled from the modusa signal and plugin framework**.

.. code-block::

    modusa/
        tools/
            my_tool.py


Basic Engine Example
--------------------

Let’s say we want to build an amplifier. The tool looks like:

.. code-block:: python

    # modusa/tools/amplifier.py

    class Amplifier:
        """
        Amplifies a given array.
        """
        @staticmethod
        def amplify(self, y: np.ndarray, gain: float = 1.0) -> np.ndarray:
            y *= gain
            return y

Key Points:

- Tool should take clean inputs and return clean outputs.
- Avoid direct dependency on plugins or decorators.


Connecting Tool to Plugin
-------------------------

Now that you have the tool, use it inside your plugin’s `apply()` method.

.. code-block:: python

    from modusa.plugins.base import ModusaPlugin
    from modusa.decorators import plugin_safety_check

    class AmplifyPlugin(ModusaPlugin):
        @property
        def allowed_input_signal_types(self):
            from modusa.signals.base import Signal1D
            return (Signal1D, )

        @property
        def allowed_output_signal_types(self):
            from modusa.signals.base import Signal1D
            return (Signal1D, )

        @plugin_safety_check()
        def apply(self, signal: "Signal1D", gain: float = 1.0) -> "Signal1D":
            from modusa.signals.base import Signal1D
            from modusa.tools.amplifier import Amplifier
            return Amplifier.amplify(y=signal.y, gain=gain)

✅ This makes the plugin reusable and logic-free. Any CLI or GUI can now directly use the `Amplifier` too.

Testing Tool
------------

You can now unit test the tool without touching plugins:

.. code-block:: python

    from modusa.tools.amplifier import Amplifier
    import numpy as np

    def test_amplifier():
        y=np.array([1, 2, 3])
        y_amplified = Amplifier.amplify(y, gain=3)
        assert all(y_amplified == np.array([3, 6, 9]))

This makes testing fast, independent, and framework-free.

Summary
-------

- ✅ Create all core logic in `modusa.engines`.
- ✅ Keep plugins thin and delegate work to engines.
- ✅ Test engines directly.
- ❌ Do **not** put complex logic directly in plugin `apply()` methods.

This architecture promotes modularity, testability, and maintainability across the Modusa ecosystem.
