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
            "--no-ansi",
            "--sync",
            f"--only={groups_formated}",
            external=True,
        )
    else:
        session.run_always(
            "poetry",
            "install",
            "--no-ansi",
            "--sync",
            f"--without={groups_formated}",
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
    install(session, without=True, groups=["lint", "dev"])
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
        groups=["lint", "typing", "nox", "dev"],
    )
    session.run("pytest", *args)


@nox.session()
def security_checks(session: nox.Session) -> None:
    """Security Checks"""
    session.run(
        "poetry",
        "install",
        "--no-ansi",
        "--sync",
        external=True,
    )
    try:
        session.run("docker", "ps", external=True)
        try:
            session.run("vulcan-local", "-c", "vulcan.yaml", "-s", "LOW", external=True)
        except:
            session.run(
                "bash",
                "-c",
                (
                    "curl -sfL https://raw.githubusercontent.com/"
                    "adevinta/vulcan-local/master/script/get | sh"
                ),
                external=True,
            )
            session.run("vulcan-local", "-c", "vulcan.yaml", "-s", "LOW", external=True)
    except:
        session.log("No docker runnig, skiped security checks")
