install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

page-loader:
	poetry run page-loader

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest -vv

coverage:
	poetry run coverage xml