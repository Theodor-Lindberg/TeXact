# TeXact

TeXact is a tool for finding miscellaneous mistakes in LaTeX code
and article writing.
It does not edit your files, so you can run it fearlessly.
It is also not intended to replace existing tools, such as
[ChkTeX](https://www.nongnu.org/chktex/) and
[lacheck](https://linux.die.net/man/1/lacheck), but rather to
complement and incorporate them.

## Documentation

[https://theodor-lindberg.github.io/TeXact/](https://theodor-lindberg.github.io/TeXact/)

## Installation

TeXact can be installed using pip, either directly from git:

```bash
python -m pip install "git+ssh://git@github.com/Theodor-Lindberg/TeXact.git"
```

or after cloning the repository:

```bash
python -m pip install .
```

## Usage

After installing, run TeXact from the command line:

```bash
texact -f path/to/file.tex
```

For more information, run

```bash
texact -h
```

## Current reviewers

1. **Unsure:** Avoid should|would|could|might.
2. **RefLabel:** Checks consistency between "\ref" and "\label".
3. **InThis:** Don't start the abstract with "In this work" or similar.
4. **Casing:** Make sure certain words have correct casing.
5. **Figure:** Things related to figures.
6. **ChkTeX:** Runs ChkTeX checks.
