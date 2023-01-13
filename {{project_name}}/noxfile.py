from typing import Iterable

import nox

nox.options.reuse_existing_virtualenvs = True

SCAN_PATHS = ["src", "tests", "noxfile.py"]


def install(
    session: nox.Session, *, groups: Iterable[str], without: bool = False
) -> None:
    """Install the dependency groups using Poetry."""
    groups_formated = ",".join(groups)
    if not without:
        session.run_always(
            "poetry",
            "install",
            "--sync",
            f"--only={groups_formated}",
            "--no-ansi",
            external=True,
        )
    else:
        session.run_always(
            "poetry",
            "install",
            "--sync",
            f"--without={groups_formated}",
            "--no-ansi",
            external=True,
        )


@nox.session()
def precommit(session: nox.Session) -> None:
    """Run Pre-commit in all files"""
    args = session.posargs or ["run", "--all-files"]
    install(session, groups=["dev"])
    session.run("pre-commit", *args)


@nox.session()
def typing(session: nox.Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or SCAN_PATHS
    install(session, without=True, groups=["lint", "dev", "deploy"])
    session.run("mypy", *args)


@nox.session()
def lint(session: nox.Session) -> None:
    """Style-check using pylint."""
    args = session.posargs or SCAN_PATHS
    install(session, groups=["lint"])
    session.run("pylint", *args)


@nox.session()
def tests(session: nox.Session) -> None:
    """Tests using pytest."""
    args = session.posargs
    install(
        session,
        without=True,
        groups=["codestyle", "lint", "typing", "nox", "dev"],
    )
    session.run("pytest", *args)
    session.run("coverage", "xml")
    session.run("coverage", "html")
