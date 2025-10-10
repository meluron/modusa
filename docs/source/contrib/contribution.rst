Contribution
============

We welcome all kinds of contributions! Whether you're a developer, tester, writer, or bug hunter, there's a place for you in the **modusa** project.

.. admonition:: **Steps to setup the project locally for contribution:**

	1. **Fork** the repository on GitHub.
	2. **Clone** your fork locally:
	
			.. code-block:: bash
			
				git clone https://github.com/your-username/modusa.git
				
	3. **Set up your environment**:
	
			.. code-block:: bash
			
				cd modusa
				python -m venv .venv # use python version >= 3.10
				source .venv/bin/activate  # or .venv\Scripts\activate on Windows
				pdm install # or pip install -e .
				
----

.. admonition:: **You can contribute to Modusa in many ways:**

	- **As a Developer**  
		Add new features to the codebase.
		
	- **As a Tester**
		Test the behavior of engines, plugins, signals, and generators. Write test cases or report bugs with reproducible examples.
		
	- **As a Bug Fixer**
		Pick an open issue or inspect the codebase for possible bugs. Submit patches with clean, descriptive commits.
		
	- **As a Documentation Contributor**
		Improve doc clarity, fix typos, or contribute new tutorials and guides. Good docs help everyone.
		
	- **As an Idea Contributor**
		Suggest new signal types, transformation logic, or plugins that could expand the modusa ecosystem.
		
----

.. admonition:: **Some general guidelines that you should follow:**

	- Write modular, readable, and well-documented code.
	- Follow existing naming conventions and project structure.
	- Add tests for any new functionality you introduce.
	- Use meaningful and concise commit messages.
	- If in doubt, open a GitHub issue or discussion before starting work.
	- Be kind and constructive, we value respectful collaboration.