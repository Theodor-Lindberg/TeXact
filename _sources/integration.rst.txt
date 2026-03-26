Integration
===========

TeXact can be integrated in several different ways in existing workflows.

Pre-commit hook
---------------

Continuous integration
---------------------

TeXstudio
---------

TeXact can be invoked from TeXstudio and have it's output in the messages log.

In Options->Configure TeXstudio...->Build, add a user command.
Set the name to ``texact:texact`` and let it execute ``texact --no-chktex --html-style -f ?ame``.
If you have chktex installed, you can remove ``--no-chktex``.
Press OK to save the settings.

TeXact can now be invoked on the current file under Tools->User->texact.
