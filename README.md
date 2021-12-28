# Internship search platform backend

## Development

### Recommended setup

- Install [`poetry`](https://github.com/python-poetry/poetry#installation) and [`pyenv`](https://github.com/pyenv/pyenv)
- `pyenv install 3.9.9`
- `pyenv local 3.9.9`
- `poetry install`
- `poetry run pre-commit install`
- Run the application using `poetry run python -m backend`.

If you need to activate the resulting virtual environment for your current shell, simply use `poetry shell`.

### Pre-commit

```sh
poetry run pre-commit install
```

The pre-commit hook will now automatically run whenever you use `git commit`.
If you want to run it manually, use:

```sh
poetry run pre-commit run --all-files
```
