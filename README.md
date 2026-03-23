# TeXact

TeXact is a tool for finding miscellaneous mistakes in LaTeX code
and article writing.

## Installation

TeXact can be installed using pip:

```bash
python -m pip install .
```

or directly from git:

```bash
python -m pip install "git+ssh://git@github.com/Theodor-Lindberg/TeXact.git"
```

## Usage

After installation, run TeXact from the command line:

```bash
texact -f path/to/file.tex
```

For more information, run

```bash
texact -h
```

## Current reviewers

1. **Ould:** Avoid should|would|could.
2. **RefLabel:** Checks consistency between "\ref" and "\label".
3. **InThis:** Don't start the abstract with "In this work" or similar.
4. **Casing:** Make sure some words have correct casing.
5. **Figure:** Things related to figures.

## Contributing

### Code structure

The tool is implemented as a set of reviewers, each with its own
focus. The reviewers keep track of their comments as the LaTeX file is
processed line by line.
Once the entire file has passed, all comments are printed to the
console, referencing line numbers.
A summary is also outputted at the end.

### Adding a reviewer

All reviewers inherit from the same base class, *Reviewer*, and
implements a set of methods: `process_line`, `get_comments`,
`get_summary`, `get_status`, and `get_name`.
The easiest way to get started is to copy one of the existing classes,
e.g. `Reviewer_ould`.
The main file, `texact`, must then be updated to include the reviewer.
Command line arguments can be added as well, if necessary.
