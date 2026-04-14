from pathlib import Path

import pytest
from conftest import SINGLE_CI_GITHUB_WORKFLOW, DefaultUserAnswer
from copier import run_copy


def test_copier_excludes_github_when_ci_github_false(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(ci_github=False)
    cwd = Path(__file__).resolve().parent.parent

    run_copy(
        src_path=str(cwd),
        dst_path=tmp_path,
        unsafe=True,
        data=given.model_dump(),
        vcs_ref="HEAD",
    )
    _ = capsys.readouterr()

    github_dir = tmp_path / ".github"
    assert not github_dir.exists()


def test_copier_excludes_gitlab_ci_when_ci_gitlab_false(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(ci_gitlab=False)
    cwd = Path(__file__).resolve().parent.parent

    run_copy(
        src_path=str(cwd),
        dst_path=tmp_path,
        unsafe=True,
        data=given.model_dump(),
        vcs_ref="HEAD",
    )
    _ = capsys.readouterr()

    gitlab_ci_file = tmp_path / ".gitlab-ci.yml"
    assert not gitlab_ci_file.exists()


def test_copier_excludes_docs_when_include_docs_false(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(include_docs=False)
    cwd = Path(__file__).resolve().parent.parent

    run_copy(
        src_path=str(cwd),
        dst_path=tmp_path,
        unsafe=True,
        data=given.model_dump(),
        vcs_ref="HEAD",
    )
    _ = capsys.readouterr()

    docs_dir = tmp_path / "docs"
    zensical_file = tmp_path / "zensical.toml"
    assert not docs_dir.exists()
    assert not zensical_file.exists()


def test_copier_excludes_license_when_copyright_license_is_none(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(copyright_license="None")
    cwd = Path(__file__).resolve().parent.parent

    run_copy(
        src_path=str(cwd),
        dst_path=tmp_path,
        unsafe=True,
        data=given.model_dump(),
        vcs_ref="HEAD",
    )
    _ = capsys.readouterr()

    license_file = tmp_path / "LICENSE"
    assert not license_file.exists()


def test_copier_excludes_missing_workflows(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(ci_github_workflows=SINGLE_CI_GITHUB_WORKFLOW)
    cwd = Path(__file__).resolve().parent.parent

    run_copy(
        src_path=str(cwd),
        dst_path=tmp_path,
        unsafe=True,
        data=given.model_dump(),
        vcs_ref="HEAD",
    )
    _ = capsys.readouterr()

    workflows_dir = tmp_path / ".github" / "workflows"
    assert workflows_dir.exists()

    expected_workflow = "test_coverage.yml"
    excluded_workflows = [
        "code_quality.yml",
        "docs.yml",
        "publish.yml",
        "release.yml",
        "test_platform.yml",
    ]

    assert (workflows_dir / expected_workflow).exists()
    for workflow in excluded_workflows:
        assert not (workflows_dir / workflow).exists()
