brew install pipx
pipx ensurepath
pipx install poetry
poetry init

poetry add --group dev pytest
poetry add --group dev flake8
poetry add --group dev black
poetry add --group dev mypy
poetry add --group dev pre-commit

poetry run pre-commit migrate-config
poetry run pre-commit install

