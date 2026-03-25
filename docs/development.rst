Development
===========

Code structure
--------------

The tool is implemented as a set of reviewers, each with its own
focus. The reviewers keep track of their comments as the LaTeX file is
processed line by line.
Once the entire file has passed, all comments are printed to the
console, referencing line numbers.
A summary is also outputted at the end.
As the reviewers are independent of one another, adding new ones
shouldn't break existing features.

Adding a reviewer
-----------------

All reviewers inherit from the same base class, *Reviewer*, and
implements a set of methods: ``process_line``, ``get_comments``,
``get_summary``, ``get_status``, and ``get_name``.
The easiest way to get started is to copy one of the existing classes,
e.g. ``Reviewer_ould``.
The main file, ``texact``, must then be updated to include the reviewer.
Command-line arguments can be added as well, if necessary.
