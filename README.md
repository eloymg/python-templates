# Python General Template

This repository serves as a template for creating a general Python repository using [Copier](https://github.com/clab/copier). It includes a basic file structure and some common dependencies for Python projects such as [poetry](https://python-poetry.org/), [nox](https://nox.thea.codes/), [pylint](https://www.pylint.org/), [mypy](http://mypy-lang.org/) and [pre-commit](https://pre-commit.com/).

## Getting Started

1. Install Copier: 
   ```
   pip install copier
   ```
2. Install Poetry: 
   ```
   curl -sSL https://install.python-poetry.org | python -
   ```
3. Run the following command to create a new project using the template: 
   ```
    copier https://github.com/eloymg/python-templates.git <destination_path>
   ```
4. Follow the prompts to provide a name and location for the new project.
5. Once the project is created, navigate to the project directory and enable virtual enviroment using poetry: 
    ```
    poetry shell
    ```

## Usage

### Poetry

The project uses Poetry for dependency management. To add/update/remove a dependency:
```sh
poetry add/update/remove <dependency>
```

### Nox

The project uses Nox to automate common tasks such as linting, testing, and building. To see the available commands, run:
```sh
nox
```

### Pylint, Mypy, Pytest and pre-commit

This template also includes Pylint, Mypy and pre-commit for linting, type checking and commit hooks respectively, you can run them with nox or by invoking them directly:
```sh
pylint <files_path>
mypy <files_path>
pre-commit run --all-files
pytest
```

## Contributing

Please feel free to submit pull requests and issues. 

## Licensing

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
