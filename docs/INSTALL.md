# Install development environment for project

### To do it, you must have some tools:
- [uv](https://docs.astral.sh/uv/)
- [poetry](https://python-poetry.org/docs/)
- [docker](https://docs.docker.com/)

If you use zsh, command below provide autocomplete for invoke command

```
source <(inv --print-completion-script zsh)
```

## Installation

1. Install environment

```
uv venv --python 3.12 && poetry install && source .venv/bin/activate
```
2. Setup project
```
inv project.init
```
3. Run project locally
```
inv fastapi.run
```
