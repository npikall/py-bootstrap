from pathlib import Path

import pytest
from conftest import FullUserAnswers
from copier import run_copy


def test_zensical_copies_correct_files(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = FullUserAnswers(docs_engine="zensical")
    cwd = Path(__file__).resolve().parent.parent

    # Run copier with the given context
    run_copy(
        src_path=str(cwd),
        dst_path=tmp_path,
        unsafe=True,
        data=given.model_dump(),
        vcs_ref="HEAD",
    )
    _ = capsys.readouterr()

    want = ["index.md"]
    for file in want:
        filepath = tmp_path / "docs" / file
        assert filepath.exists()


def test_mkdocs_copies_correct_files(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = FullUserAnswers(docs_engine="mkdocs")
    cwd = Path(__file__).resolve().parent.parent

    # Run copier with the given context
    run_copy(
        src_path=str(cwd),
        dst_path=tmp_path,
        unsafe=True,
        data=given.model_dump(),
        vcs_ref="HEAD",
    )
    _ = capsys.readouterr()

    want = ["index.md", "license.md", "contributing.md", "changelog.md"]
    for file in want:
        filepath = tmp_path / "docs" / file
        assert filepath.exists()
