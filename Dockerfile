FROM mwalbeck/python-poetry:1.8-3.12

WORKDIR /app/

COPY ./src /app/

COPY pyproject.toml poetry.lock /app/

RUN poetry install
RUN poetry show
