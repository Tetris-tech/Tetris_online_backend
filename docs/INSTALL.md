# Install development environment for project

### To do it, you must have some tools

- [uv](https://docs.astral.sh/uv/)
- [poetry](https://python-poetry.org/docs/)
- [docker](https://docs.docker.com/)
- [pack-cli](https://buildpacks.io/docs/for-platform-operators/how-to/integrate-ci/pack/)
- [make utility](https://www.gnu.org/software/make/)

If you use zsh, command below provide autocomplete for invoke command

```
source <(inv --print-completion-script zsh)
```

## Installation (wihout buildpack)

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

## Installation (with buildpack)

1. Build image via buildpack

```
make build
```

2. Run application

```
make up
```
P.S.: Other commands with `make` see in `Makefile`

## Installation (with k8s)

Soon...
