FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# package dependency manager `poetry` without environment isolation (It is a job of Docker.)
ENV POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://install.python-poetry.org | python3 -