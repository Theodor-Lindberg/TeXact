.. TeXact documentation master file

Welcome to TeXact's documentation!
==================================

TeXact is a tool for finding miscellaneous mistakes in LaTeX code and article writing.

The repository can be found at `GitHub <https://github.com/Theodor-Lindberg/TeXact>`_. Please
report any issues or suggestions there. Contributions are also welcome!

Installation
------------

TeXact can be installed using pip, either directly from git or after cloning the repository.

.. admonition:: Install APyTypes from git

    .. code-block:: console

        $ python -m pip install "git+ssh://git@github.com/Theodor-Lindberg/TeXact.git"

.. admonition:: Install TeXact after cloning

    .. code-block:: console

        $ python -m pip install .

Usage
-----

After installing, run TeXact from the command line:

```
texact -f path/to/file.tex
```

For more information, run

```
texact -h
```


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   checklist
   development



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. image:: _static/texactlogo-white.svg
   :class: only-dark
   :scale: 500%

.. image:: _static/texactlogo-black.svg
   :class: only-light
   :scale: 500%
