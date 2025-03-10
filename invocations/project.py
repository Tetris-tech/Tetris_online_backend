import invoke
import saritasa_invocations


@invoke.task
def init(
    context: invoke.Context,
    clean: bool = False,
) -> None:
    """Setup project."""
    saritasa_invocations.print_success("Start project setup")

    if clean:
        saritasa_invocations.docker.clear(context)

    saritasa_invocations.docker.up(context)
    saritasa_invocations.alembic.upgrade(context)
    saritasa_invocations.print_success("Project setup is completed")


@invoke.task
def restart(
    context: invoke.Context,
) -> None:
    ("Restart project",)
    saritasa_invocations.print_success("Start project restart")
    init(context, clean=True)
    saritasa_invocations.print_success("Restart is completed")
