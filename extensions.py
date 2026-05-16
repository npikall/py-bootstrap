import re
import subprocess
import sys
import unicodedata

from jinja2.ext import Extension


def read_target_from_args() -> str:
    args = sys.argv
    last = args[-1]
    before_last = args[-2]
    if not is_option(before_last) and not is_option(last):
        return last
    return ""


def is_option(arg: str) -> bool:
    return arg.startswith("-")


def git_user_name(default: str) -> str:
    cmd = "git config user.name"
    return subprocess.getoutput(cmd).strip() or default  # noqa: S605


def git_user_email(default: str) -> str:
    cmd = "git config user.email"
    return subprocess.getoutput(cmd).strip() or default  # noqa: S605


def slugify(value: str, separator: str = "-") -> str:
    value = (
        unicodedata.normalize("NFKD", str(value))
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-_\s]+", separator, value).strip("-_")


class GitExtension(Extension):
    def __init__(self, environment):  # noqa: ANN001, ANN204
        super().__init__(environment)
        environment.filters["git_user_name"] = git_user_name
        environment.filters["git_user_email"] = git_user_email
        environment.globals["read_target_from_args"] = read_target_from_args


class SlugifyExtension(Extension):
    def __init__(self, environment):  # noqa: ANN001, ANN204
        super().__init__(environment)
        environment.filters["slugify"] = slugify
