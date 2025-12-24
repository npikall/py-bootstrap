from datetime import datetime
from pathlib import Path

import pytest
from copier import run_copy
from pydantic import BaseModel


class UserAnswers(BaseModel):
    project_name: str = "example"
    author_fullname: str = "John Doe"
    author_email: str = "john.doe@mail.com"
    author_username: str = "jdoe"
    ci_github: bool = True
    ci_gitlab: bool = True
    repo_name: str = "example"
    include_docs: bool = True
    docs_generator: str = "zensical"
    pre_commit: str = "prek"


class ChooseLicense(UserAnswers):
    copyright_license: str


CUR_YEAR = datetime.today().year  # noqa: DTZ002


def test_license_MIT_renders_correct(  # noqa: N802
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = ChooseLicense(copyright_license="MIT")
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

    license_file = tmp_path / "LICENSE"
    assert license_file.exists()

    got = license_file.read_text()
    assert "MIT License" in got
    assert f"Copyright (c) {CUR_YEAR} John Doe" in got


def test_license_apache_renders_correct(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = ChooseLicense(copyright_license="Apache-2.0")
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

    license_file = tmp_path / "LICENSE"
    assert license_file.exists()

    got = license_file.read_text()
    assert "Apache License" in got
    assert "Version 2.0, January 2004" in got
    assert f"Copyright {CUR_YEAR} John Doe" in got


def test_license_unlicense_renders_correct(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = ChooseLicense(copyright_license="Unlicense")
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

    license_file = tmp_path / "LICENSE"
    assert license_file.exists()

    got = license_file.read_text()
    assert "This is free and unencumbered software released into the" in got
