from pathlib import Path
import subprocess

import pytest
from printer import Printer
from reviewer import Status
from reviewer_unsure import Reviewer_Unsure


TEST_DIR = Path(__file__).resolve().parent
TEX_FILES = sorted(TEST_DIR.glob("*.tex"))


def test_tex_fixtures_exist() -> None:
    assert TEX_FILES, "No .tex files found in test_files/"


@pytest.mark.parametrize("tex_file", TEX_FILES, ids=lambda tex_file: tex_file.name)
def test_texact_no_crash_for_tex_file(tex_file: Path) -> None:
    result = subprocess.run(
        ["texact", str(tex_file)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1, (
        f"texact crashed for {tex_file}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )


def test_reviewer_unsure_fails_on_space_before_period() -> None:
    reviewer = Reviewer_Unsure(Printer())
    reviewer.process_line(0, "The frequency . is measured.")

    assert reviewer.get_status() == Status.FAILED
    assert reviewer.get_summary() == "Spaces before period: 1"


def test_reviewer_unsure_passes_without_space_before_period() -> None:
    reviewer = Reviewer_Unsure(Printer())
    reviewer.process_line(0, "The frequency. is measured.")

    assert reviewer.get_status() == Status.PASSED
    assert reviewer.get_summary() == ""
