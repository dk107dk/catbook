brew install pipx
pipx ensurepath
pipx install poetry
poetry init

poetry add --dev pytest
poetry add --dev flake8
poetry add --dev black
poetry add --dev mypy
poetry add --dev pre-commit

poetry run pre-commit migrate-config
poetry run pre-commit install

