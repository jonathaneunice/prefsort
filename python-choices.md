# Python project constitution

A portable set of defaults for modernizing a **publishable Python library** to 2026 tooling. Apply every later section as the default. Do not relitigate a choice that already has a one-line why.

Worked example throughout: **prefsort** (a small typed library, Apache-2.0, Python 3.11+, GitHub, PyPI). The living example is this repo; `pyproject.toml` is the source of truth for name, description, authors, license, and Python floor.

## How to apply

1. Copy this file into the target repo as `python-choices.md`.
2. Leave bracketed tokens as holes, or substitute from the *target’s* `pyproject.toml` and git remote. Do not copy prefsort’s name, author, license, or description. Do not invent a new name or license. Convert a landing `README.rst` to `README.md`; do not keep both.
3. Apply every section as written. Where the target cannot comply yet, record the gap in `residual.md` (see [Working leftovers](#working-leftovers)) rather than quietly weakening the rule.
4. Do not resurrect the [retired stack](#retired-on-purpose).
5. These are defaults. The user may request a variance or exception which is fine. If so, add an Exceptions section at the end of this document with exceptions noted and the date recorded in YYYY-MM-DD format.

---

## Language and runtime

- Python 3 only. `[MIN_PYTHON]` is **3.11**. `[CURRENT_PYTHON]` is the newest **released** CPython. Claim every released minor from there through that version. The test matrix may also include the next minor once it is in beta/RC; do not add that version’s Trove classifier or use it for the build job until it is released.
- Claim **CPython only** (`Programming Language :: Python :: Implementation :: CPython`). Do not add PyPy, universal wheels, or a 2/3 compatibility layer unless spefically requested. 
- Write modern Python 3.11 idioms: `X | Y` unions, and built-in generics such as `list[T]`, `TypeVar`. Use `from __future__ import annotations` where deferred annotations are useful (Python 3.11–3.13); don't add it mechanically.
- Import abstract containers from `collections.abc`, not `typing`.

---

## Layout

Snippets use `[PROJECT]` as a stand-in for the distribution and import name (keep those the same unless the target already splits them). Other bracketed tokens are holes to fill from the target’s `pyproject.toml` and git remote, not a second metadata registry.

```
[PROJECT]/
  pyproject.toml          # only config file for packaging and tools
  Makefile                # only documented command interface
  README.md
  CHANGELOG.md
  LICENSE
  NOTICE                  # when [LICENSE_SPDX] is Apache-2.0
  MANIFEST.in             # only files setuptools would otherwise omit
  python-choices.md
  residual.md             # working leftovers, not constitution
  src/[PROJECT]/
    __init__.py           # public re-exports and __all__
    py.typed
    version.py            # __version__ from importlib.metadata
    ...
  tests/                  # pytest; no tests/__init__.py
  .github/workflows/ci.yml
  .github/dependabot.yml
  .gitignore
```

- **src layout.** Keeps an editable install honest: tests and `python [PROJECT]/...` cannot accidentally import the tree instead of the package.
- Tests live in `tests/`, not `test/`.
- No `docs/` Sphinx tree for a library whose README, docstrings, and changelog already are the documentation. Use `docs/` however if present or requested.

---

## Packaging

Single source: `pyproject.toml`. No `setup.py`, `setup.cfg`, or `requirements*.txt`.

```toml
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "[PROJECT]"
version = "0.2.0"          # static; see Versioning
description = "[DESCRIPTION]"
readme = "README.md"
requires-python = ">=[MIN_PYTHON]"
license = "[LICENSE_SPDX]"
license-files = ["LICENSE"]  # plus "NOTICE" when Apache-2.0
```

- **setuptools >= 77** for PEP 639 `license` / `license-files`. Do not use `License :: OSI Approved :: ...` classifiers.
- Authors, keywords, and URLs live in `[project]`, not in `__init__.py`. Do not keep `__author__`, `__email__`, or create an `AUTHORS` file unless requested.
- Required classifiers: `Programming Language :: Python :: 3 :: Only`, one classifier per supported minor, `Typing :: Typed`, plus audience/topic/status that match reality.
- `[project.urls]`: Homepage, Changelog, Issues, Source.
- `[tool.setuptools.packages.find] where = ["src"]`.
- `[tool.setuptools.package-data] [PROJECT] = ["py.typed"]`.
- Runtime dependencies go in `[project.dependencies]`. An empty list is written explicitly as `dependencies = []`, not omitted.
- `MANIFEST.in` lists only extras the sdist would miss. Ship `CHANGELOG.md` that way. Do not use it as a cookiecutter junk drawer.

---

## Dependencies and install

PEP 735 **dependency groups**, not extras, not requirements files. Extras are for runtime optional features; dev tools are not features.

```toml
[dependency-groups]
test = ["pytest>=8", "pytest-cov>=5"]
quality = [
    "actionlint-py>=1.7.7",
    "mypy>=1.15",
    "pre-commit-hooks>=6",   # check-yaml / check-toml CLIs, not git hooks
    "ruff>=0.15.10",
    "shellcheck-py>=0.10",
    "validate-pyproject>=0.24",
]
build = ["build>=1.2", "twine>=6"]
dev = [
    { include-group = "test" },
    { include-group = "quality" },
    { include-group = "build" },
]
```

- Require **pip >= 25.1** so `pip install --group` works.
- Documented install: create a venv, then `make install` → `pip install --group dev -e .`.
- Quality checkers install with the project. `make lint` must work after `make install` with no extra bootstrap.
- **pip is the installer.** Do not add Poetry, Hatch, PDM, or uv as a required project frontend. Do not add tox; the CI matrix is the multi-version story.

---

## Code and types

- Type every public function and every test. Ship `py.typed`. Run **mypy `--strict`** plus `warn_unreachable` on `src/[PROJECT]` and `tests`, with `python_version = "[MIN_PYTHON]"`.
- Re-export the public API from `__init__.py` and name it in `__all__`.
- Google-style `Args:` / `Returns:` on public callables. Put executable `Examples:` doctests on the public surface.
- Prefer a small, exact contract over hidden performance claims. If scale or a sharp edge matters, say so in the docstring.
- Docstrings put the text on its own lines between the quotes, even when the text is one sentence. Do not collapse to `"""comment"""`. This is easier to extend and to scan; Ruff format preserves the layout, and pydocstyle `D200` is not enabled because it would fight it.

```python
"""
Public interface for :mod:`[PROJECT]`.
"""
```

---

## Quality tools

Ruff both lints and formats. mypy types. pip-wrapped checkers cover YAML, TOML, and workflows. No git hooks.

```toml
[tool.ruff]
line-length = 108
target-version = "py311"   # [MIN_PYTHON] without the dot

[tool.ruff.lint]
select = ["B", "E4", "E7", "E9", "F", "I", "PT", "RUF", "SIM", "UP", "W"]

[tool.ruff.format]
quote-style = "double"
```

- **108 columns**, double quotes, Ruff format (Black-compatible). Do not add Black, isort, or flake8 beside Ruff.
- Lint select is this set, not the kitchen sink. mypy owns annotations; do not enable Ruff `ANN`.
- `W` covers trailing whitespace and a missing final newline in Python. That is enough; do not add a second whitespace tool for Python, or a checker for other tracked text.
- `make lint` also runs:
  - `check-yaml .github/workflows/*.yml .github/dependabot.yml`
  - `check-toml pyproject.toml`
  - `validate-pyproject pyproject.toml`
  - `actionlint -verbose`
- `actionlint-py` and `shellcheck-py` are pip wrappers that fetch their binaries at install time. Do not require a separate Go/system install.
- **No pre-commit.** Lint runs when someone types `make lint` or when CI does. Do not add `.pre-commit-config.yaml`.

---

## Tests

```toml
[tool.pytest.ini_options]
addopts = ["--strict-config", "--strict-markers", "-ra", "--doctest-modules"]
filterwarnings = ["error"]
testpaths = ["src", "tests"]

[tool.coverage.run]
branch = true
source = ["[PROJECT]"]

[tool.coverage.report]
fail_under = 100
show_missing = true
skip_covered = false
```

- pytest only. Assertions, `parametrize` for variants, test names that state the contract (`test_does_not_mutate_input`).
- **100% branch coverage** is the gate. `make test` always runs with coverage. `skip_covered = false` so fully covered files still appear in the table; `skip_covered` only hides rows from the report, it does not skip tests.
- `filterwarnings = ["error"]` so a new warning is a failed test, not log noise.
- `--doctest-modules` plus `testpaths` including `src` executes docstring examples. README Python examples have their own test that executes every fenced block tagged `python` and asserts the extracted-block count equals the opening-fence count, so a broken fence cannot silently skip a block. Ignore `console` and other non-Python fences.
- Cover behavior at the public seam (return value, new list vs alias, iterator consumed once, no mutation). Do not test private helpers through a back door if the public function is the product.

---

## Makefile

The Makefile is the human and CI interface. Default target is `help`. Parameterize the interpreter as `PYTHON ?= python3`.

| Target | Does |
| --- | --- |
| `install` | Upgrade pip to >= 25.1; `pip install --group dev -e .` |
| `format` | `ruff check --fix` then `ruff format` |
| `lint` | check (not fix): Ruff lint, Ruff format `--check`, mypy, YAML/TOML/schema/actionlint |
| `test` | pytest with coverage |
| `test-cov` | as `test`, plus HTML report opened locally |
| `build` | `rm -rf dist`, `python -m build`, `twine check --strict dist/*` |
| `check` | `lint` then `test` |
| `require-clean-tree` | fail unless `git status --porcelain` is empty |
| `publish-test` / `publish` | `check`, clean tree, `build`, twine upload |

- `format` writes; `lint` only reports. CI runs `lint`, never `format`.
- `test-cov` is a local convenience (`open` on macOS in prefsort). CI does not use it.
- Do not hide a second set of commands in the README. `make help` is the catalog.

---

## Continuous integration

One workflow: `.github/workflows/ci.yml`. No Travis, no tox.

```yaml
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

- Least privilege: `contents: read` only.
- Cancel superseded runs on the same ref. Job `timeout-minutes: 10`.
- **test** job: matrix of every supported CPython (`[MIN_PYTHON]` … `[CURRENT_PYTHON]`), plus the next minor in beta/RC when one exists (`3.15` today). `fail-fast: false`, `ubuntu-latest`, `actions/checkout@v6`, `actions/setup-python@v6` with `cache: pip` and `allow-prereleases: true` so the unreleased cell installs. Then the same commands as a human: `make install`, `make lint`, `make test`.
- **build** job: `[CURRENT_PYTHON]` only (the latest *release*, not an RC). Install the `build` group, `make build`, upload `dist/` with `actions/upload-artifact@v6`.
- Float Actions on major tags (`@v6`). CI must use the Makefile targets so local and CI cannot drift.
- **Dependabot** keeps those tags from aging. Ship `.github/dependabot.yml` for the `github-actions` ecosystem on a weekly schedule. `actionlint` checks workflow syntax; it does not bump versions. Dependabot opens a PR when `checkout` / `setup-python` / `upload-artifact` (etc.) publish a new major; that PR runs CI because of `on: pull_request`. Do not add a pip ecosystem here unless the project wants the same treatment for `pyproject.toml` tools.

---

## Documentation

- **README.md** is the PyPI long description and the human landing page. Greenfield default is GitHub-flavored Markdown. Convert an existing `README.rst` rather than keeping both files.
- **CHANGELOG.md** is Markdown too. One dated heading per released version, newest first, user-visible bullets.
- README structure: title, GFM badges (PyPI version, Python versions, CI), short pitch with the Python requirement, install, usage with fenced `python` / `console` examples, a short Development section that points at `make install` / `make check` / `make format` / `make help`.
- Do not document a releasing ritual in the README. The Makefile is the source of truth; README copy of it will rot.
- Examples in README and public docstrings are tests (see [Tests](#tests)).
- No `AUTHORS` file; authors are `[project.authors]`.

---

## License

- Keep the target’s existing license. If it has none, use **Apache-2.0**.
- Ship the **full license text**, not a stub that only names the license.
- PEP 639: `license = "[LICENSE_SPDX]"` and `license-files`. For Apache-2.0, `license-files = ["LICENSE", "NOTICE"]` and a short `NOTICE` with copyright.
- Do not also list a license Trove classifier. PEP 639 obsoleted that approach.

---

## Versioning and release

Declare `version` **statically** in `[project]` of `pyproject.toml`. Expose it at runtime with:

```python
from importlib.metadata import version

__version__ = version("[PROJECT]")
```

Packaging metadata is the source of truth; a second `__version__ = "…"` in source will drift from the built artifact. A bump is visible to the interpreter only after reinstall; that is accepted. Builds and uploads read `pyproject.toml` directly and are unaffected.

- No bumpversion / commit-and-tag version tools. Edit `pyproject.toml`, date `CHANGELOG.md`, commit, tag `v[version]`.
- Publish **locally** with twine, not a GitHub `id-token` workflow:
  - `TWINE_USERNAME ?= __token__` (API token; password from the OS keyring).
  - `make publish-test` → TestPyPI; `make publish` → PyPI.
  - Both depend on `check`, `require-clean-tree`, and `build`. `build` deletes `dist/` first so a stale wheel cannot be uploaded.
- **Clean tree is mandatory for publish.** Uncommitted, unstaged, or unignored files fail the release. Why: the sdist is built from the worktree; a dirty tree means the uploaded artifact is not the tagged commit.

---

## Git hygiene

`.gitignore` is short and actual, not a cookiecutter kitchen sink:

- bytecode, `.venv/` / `venv/`
- `build/`, `dist/`, `*.egg-info/`
- `htmlcov/`, `.coverage*`, `coverage.xml`
- `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`
- `.DS_Store`, `.python-version`

Do not ignore `.github`. Do not commit `.python-version`: a local pin is not project policy; the CI matrix is. Do not add `.editorconfig` unless something other than Ruff needs it.

When editing tracked text that Ruff does not see, strip trailing whitespace and end the file with a newline. Do not add a checker or `.editorconfig` for that.

---

## Retired on purpose

When modernizing an older library (cookiecutter-pypackage and similar), delete these. Do not reintroduce them under a new name:

| Retired | Replaced by |
| --- | --- |
| `setup.py`, `setup.cfg` | `pyproject.toml` |
| `requirements_dev.txt`, extras-as-dev-tools | PEP 735 `[dependency-groups]` |
| `tox.ini`, `toxcov.ini` | GHA version matrix + `make test` |
| `.travis.yml` | `.github/workflows/ci.yml` |
| `pytest.ini` | `[tool.pytest.ini_options]` |
| Black + isort + flake8 | Ruff check + Ruff format |
| `.pre-commit-config.yaml` | `make lint` |
| `CHANGES.yml` / ad-hoc history | `CHANGELOG.md` |
| bumpversion | static `[project].version` |
| `AUTHORS.rst` / `__author__` | `[project.authors]` |
| `README.rst` as the landing page | `README.md` (GFM); tests extract fenced `python` blocks |
| `test/` (singular), `tests_require` | `tests/` + pytest |
| Dynamic version from a source attribute | `version` in `pyproject.toml` + `importlib.metadata` |
| Stub / one-paragraph `LICENSE` | Full license text (+ `NOTICE` if Apache-2.0) |
| Universal wheels, Python 2, `<3.11` | CPython `[MIN_PYTHON]+` |

---

## Working leftovers

Keep a `residual.md` for review items that are **not** yet done and are **not** this constitution. That file is a working list: ordered by value-to-effort, trimmed as items close, never a second set of defaults.

Agents applying this constitution to another project should start a fresh `residual.md` for that project’s leftovers (coverage not yet 100%, an old Python still in the wild, and so on). Do not copy another repo’s residual items forward.
