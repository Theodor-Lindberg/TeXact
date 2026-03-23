from pathlib import Path
import subprocess

import pytest


TEST_DIR = Path(__file__).resolve().parent
TEX_FILES = sorted(TEST_DIR.glob("*.tex"))


def test_tex_fixtures_exist() -> None:
    assert TEX_FILES, "No .tex files found in test_files/"


@pytest.mark.parametrize("tex_file", TEX_FILES, ids=lambda tex_file: tex_file.name)
def test_texact_no_crash_for_tex_file(tex_file: Path) -> None:
    result = subprocess.run(
        ["texact", "-f", str(tex_file), "--ould", "true"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, (
        f"texact crashed for {tex_file}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )
