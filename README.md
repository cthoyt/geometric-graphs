<!--
<p align="center">
  <img src="https://github.com/cthoyt/geometric-graphs/raw/main/docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  Geometric Graphs
</h1>

<p align="center">
    <a href="https://github.com/cthoyt/geometric-graphs/actions?query=workflow%3ATests">
        <img alt="Tests" src="https://github.com/cthoyt/geometric-graphs/workflows/Tests/badge.svg" />
    </a>
    <a href="https://github.com/cthoyt/cookiecutter-python-package">
        <img alt="Cookiecutter template from @cthoyt" src="https://img.shields.io/badge/Cookiecutter-python--package-yellow" /> 
    </a>
    <a href="https://pypi.org/project/geometric_graphs">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/geometric_graphs" />
    </a>
    <a href="https://pypi.org/project/geometric_graphs">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/geometric_graphs" />
    </a>
    <a href="https://github.com/cthoyt/geometric-graphs/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/geometric_graphs" />
    </a>
    <a href='https://geometric_graphs.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/geometric_graphs/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href='https://github.com/psf/black'>
        <img src='https://img.shields.io/badge/code%20style-black-000000.svg' alt='Code style: black' />
    </a>
</p>

Generate knowledge graphs with interesting geometries, like lattices.

## 💪 Getting Started

See https://github.com/cthoyt/translational-toys for example usage to generate
charts like 

![](https://github.com/cthoyt/translational-toys/raw/main/results/line/embedding.gif).

## 🚀 Installation

The most recent release can be installed from
[PyPI](https://pypi.org/project/geometric_graphs/) with:

```bash
$ pip install geometric_graphs
```

The most recent code and data can be installed directly from GitHub with:

```bash
$ pip install git+https://github.com/cthoyt/geometric-graphs.git
```

To install in development mode, use the following:

```bash
$ git clone git+https://github.com/cthoyt/geometric-graphs.git
$ cd geometric-graphs
$ pip install -e .
```

## 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. See
[CONTRIBUTING.rst](https://github.com/cthoyt/geometric-graphs/blob/master/CONTRIBUTING.rst) for more information on getting involved.

## 👋 Attribution

### ⚖️ License

The code in this package is licensed under the MIT License.

<!--
### 📖 Citation

Citation goes here!
-->

<!--
### 🎁 Support

This project has been supported by the following organizations (in alphabetical order):

- [Harvard Program in Therapeutic Science - Laboratory of Systems Pharmacology](https://hits.harvard.edu/the-program/laboratory-of-systems-pharmacology/)

-->

<!--
### 💰 Funding

This project has been supported by the following grants:

| Funding Body                                             | Program                                                                                                                       | Grant           |
|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------|
| DARPA                                                    | [Automating Scientific Knowledge Extraction (ASKE)](https://www.darpa.mil/program/automating-scientific-knowledge-extraction) | HR00111990009   |
-->

### 🍪 Cookiecutter

This package was created with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack) template.

## 🛠️ For Developers

<details>
  <summary>See developer instrutions</summary>

  
The final section of the README is for if you want to get involved by making a code contribution.

### ❓ Testing

After cloning the repository and installing `tox` with `pip install tox`, the unit tests in the `tests/` folder can be
run reproducibly with:

```shell
$ tox
```

Additionally, these tests are automatically re-run with each commit in a [GitHub Action](https://github.com/cthoyt/geometric-graphs/actions?query=workflow%3ATests).

### 📦 Making a Release

After installing the package in development mode and installing
`tox` with `pip install tox`, the commands for making a new release are contained within the `finish` environment
in `tox.ini`. Run the following from the shell:

```shell
$ tox -e finish
```

This script does the following:

1. Uses BumpVersion to switch the version number in the `setup.cfg` and
   `src/geometric_graphs/version.py` to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel
3. Uploads to PyPI using `twine`. Be sure to have a `.pypirc` file configured to avoid the need for manual input at this
   step
4. Push to GitHub. You'll need to make a release going with the commit where the version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump the version by minor, you can
   use `tox -e bumpversion minor` after.
</details>
