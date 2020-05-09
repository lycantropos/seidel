seidel
======

[![](https://travis-ci.com/lycantropos/seidel.svg?branch=master)](https://travis-ci.com/lycantropos/seidel "Travis CI")
[![](https://dev.azure.com/lycantropos/seidel/_apis/build/status/lycantropos.seidel?branchName=master)](https://dev.azure.com/lycantropos/seidel/_build/latest?definitionId=26&branchName=master "Azure Pipelines")
[![](https://codecov.io/gh/lycantropos/seidel/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/seidel "Codecov")
[![](https://img.shields.io/github/license/lycantropos/seidel.svg)](https://github.com/lycantropos/seidel/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/seidel.svg)](https://badge.fury.io/py/seidel "PyPI")

In what follows `python` is an alias for `python3.5` or any later
version (`python3.6` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions:
```bash
python -m pip install --upgrade pip setuptools
```

### User

Download and install the latest stable version from `PyPI` repository:
```bash
python -m pip install --upgrade seidel
```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/seidel.git
cd seidel
```

Install dependencies:
```bash
python -m pip install --force-reinstall -r requirements.txt
```

Install:
```bash
python setup.py install
```

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose release
```

Bump version
```bash
bump2version --verbose release
```

This will set version to `major.minor.patch`.

### Running tests

Install dependencies:
```bash
python -m pip install --force-reinstall -r requirements-tests.txt
```

Plain
```bash
pytest
```

Inside `Docker` container:
```bash
docker-compose up
```

`Bash` script (e.g. can be used in `Git` hooks):
```bash
./run-tests.sh
```

`PowerShell` script (e.g. can be used in `Git` hooks):
```powershell
.\run-tests.ps1
```
