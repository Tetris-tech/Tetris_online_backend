import invoke
import saritasa_invocations

import invocations

ns = invoke.Collection(
    saritasa_invocations.python,
    saritasa_invocations.docker,
    saritasa_invocations.fastapi,
    saritasa_invocations.alembic,
    saritasa_invocations.celery,
    saritasa_invocations.pytest,
    saritasa_invocations.pre_commit,
    invocations.project,
)

ns.configure(
    {
        "run": {
            "pty": True,
            "echo": True,
        },
        "saritasa_invocations": saritasa_invocations.Config(
            project_name="Tetris-online-backend",
            docker=saritasa_invocations.DockerSettings(
                main_containers=(
                    "postgres",
                ),
            ),
            fastapi=saritasa_invocations.FastAPISettings(
                app="src.main:app",
            ),
            alembic=saritasa_invocations.AlembicSettings(
                migrations_folder="migrations/versions",
            ),
            pre_commit=saritasa_invocations.PreCommitSettings(
                hooks=["pre-commit", "pre-push"],
            ),
        ),
    },
)
