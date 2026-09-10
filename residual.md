# Residual review findings

Recommendations from the September 2026 project review that have **not** been acted on.
Everything else from that review is done: the 0.2.0 version bump and changelog entry, the
index-based `prefsorted` fix and its regression test, the full Apache-2.0 `LICENSE` plus
`NOTICE`, `filterwarnings = ["error"]`, the Beta development-status classifier, the removal of
`AUTHORS.rst`, and the local `make publish` / `make publish-test` release path.

Items are ordered by the value-to-effort ratio as I judged it, not by severity. None of them are
release blockers for 0.2.0.

---

## 1. Docstring examples are not executed by any configured run

`src/prefsort/core.py` carries an `Examples:` block with two doctests. They pass, but only when
invoked by hand — no configured command collects them, so nothing stops them from drifting out of
sync with the code.

The subtlety worth knowing: adding `--doctest-modules` to `addopts` alone accomplishes **nothing**
here, because `testpaths = ["tests"]` confines collection to the test directory. I verified this —
the run stayed at 12 tests. `src` has to join `testpaths`:

```toml
[tool.pytest.ini_options]
addopts = ["--strict-config", "--strict-markers", "-ra", "--doctest-modules"]
filterwarnings = ["error"]
testpaths = ["src", "tests"]
```

With both changes the suite collects 13 items and coverage still reports 100%, so the change is
free of side effects.

## 2. README examples are unverified

The README is the PyPI long description, so a stale example there is a public-facing bug. It
contains five `.. code-block:: python` blocks whose `assert`s currently hold, but nothing checks
them.

Doctest-ifying the README would work, but it means rewriting the blocks into `pycon` form with
`>>>` prompts and expected output, which reads worse than the current `assert` style. The
alternative is to execute the blocks as they stand. I built and validated this version — it
passes, and it is clean under `mypy --strict` and the project's Ruff rule set:

```python
"""Execute the Python examples embedded in README.rst."""

import re
import textwrap
from pathlib import Path
from typing import Any, ClassVar

README = Path(__file__).parent.parent / "README.rst"

CODE_BLOCK = re.compile(r"^\.\. code-block:: python\n\n((?:(?: {4}.*)?\n)+)", re.MULTILINE)


class _FakeFrame:
    """Stand-in for the DataFrame in the column-ordering example."""

    columns: ClassVar[list[str]] = ["name", "size", "id"]

    def reindex(self, columns: list[str]) -> list[str]:
        return columns


def readme_python_blocks() -> list[str]:
    return [textwrap.dedent(match.group(1)) for match in CODE_BLOCK.finditer(README.read_text())]


def test_readme_examples_execute() -> None:
    blocks = readme_python_blocks()

    assert len(blocks) == 5

    namespace: dict[str, Any] = {"df": _FakeFrame()}
    for block in blocks:
        exec(block, namespace)
```

Two design notes. The blocks share one namespace because they build on each other — `values` is
defined in the first and reused by later ones. And the `df.reindex(...)` example references a
DataFrame that does not exist, hence the `_FakeFrame` stand-in; that keeps pandas out of the test
dependencies, which matters for a package whose selling point is having no dependencies. The
`assert len(blocks) == 5` line is deliberate: without it, a regex that silently stops matching
would turn the test into a no-op that always passes.

## 3. The string shorthand is still unsound in the type signature

`prefsorted([1, 2, 3], "2")` type-checks today and silently does nothing at runtime, because the
signature is `preferred: str | Iterable[T] | None` and the implementation does
`cast(Iterable[T], preferred.split())`. The cast is load-bearing and hides the mismatch.

Overloads narrow the string form to string sequences:

```python
@overload
def prefsorted(
    seq: Iterable[str],
    preferred: str | Iterable[str] | None = ...,
    reverse: bool = ...,
) -> list[str]: ...
@overload
def prefsorted(
    seq: Iterable[T],
    preferred: Iterable[T] | None = ...,
    reverse: bool = ...,
) -> list[T]: ...
```

**Be aware of the limit before adopting this.** I tested it against mypy strict, and it does not
reject the bad call outright. In a bare statement, `prefsorted([1, 2, 3], "2")` resolves to
`list[object]` rather than an error, because mypy is free to solve the type variable as `object`
and both `list[int]` and `str` satisfy `Iterable[object]`. What the overloads do buy is an error
as soon as the result reaches a typed context:

```python
result: list[int] = prefsorted([1, 2, 3], "2")
# error: Incompatible types in assignment (expression has type "list[str]", ...)
# error: List item 0 has incompatible type "int"; expected "str"
```

The same assignment against today's signature produces no error at all. So the overloads convert
a silent no-op into a diagnostic for any call whose result is annotated, assigned to a typed
attribute, or passed onward — most real usage — and they let the `cast` go away. They are not a
complete fix, and a complete one is not available in the type system without giving up generator
support for `preferred`. Worth doing, worth documenting the gap.

## 4. pre-commit is configured but entirely inert

`.pre-commit-config.yaml` exists, and nothing runs it. There is no CI job invoking
`pre-commit run --all-files`, and `.git/hooks/pre-commit` is not installed in this clone, so the
config currently affects nobody.

Three separate things to fix:

- **Enforcement.** Either add a CI job that runs `pre-commit run --all-files`, or drop the config
  and rely on `make lint`, which already covers the same ground plus mypy. Keeping an unenforced
  config is the worst of the three options because it looks like a guarantee.
- **Version drift.** The hook pins `ruff` at `v0.15.10` while the `quality` dependency group
  allows any `ruff>=0.11`. They agree today — the installed Ruff is exactly 0.15.10 — but nothing
  keeps them aligned, and divergence shows up as a formatting fight between the hook and
  `make lint`.
- **Coverage.** No hygiene hooks (`end-of-file-fixer`, `trailing-whitespace`, `check-yaml`,
  `check-toml`) and no mypy hook, so the hooks are strictly weaker than `make lint`.

## 5. Test gaps that 100% coverage does not reveal

Branch coverage is at 100% and the gate is enforced, which makes this a good illustration that
coverage measures executed lines rather than asserted behavior. Three documented behaviors have no
test:

- **The new-list guarantee.** `test_no_preferences_preserve_order` asserts
  `prefsorted(values, preferred) == values` but never that the result is a *different* list. The
  README and the docstring both promise a newly allocated list, so `assert result is not values`
  belongs there.
- **`reverse=True` with duplicates.** Covered separately (duplicates, and reverse) but never
  together, and the interaction is where the concatenation order could regress.
- **A generator as `preferred` is consumed exactly once.** The implementation iterates
  `preferred_items` a single time, which is what makes generator input work at all. Nothing pins
  it, so a future refactor that loops twice would pass the suite while silently breaking
  generators.

## 6. CI and repository hygiene

Small, independent items:

- **No Dependabot configuration** for GitHub Actions, so action versions age silently.
- **No `concurrency` group** with `cancel-in-progress`, so superseded pushes keep burning runners
  across the four-version matrix.
- **No `timeout-minutes`** on either job; a hung job can occupy a runner for six hours.
- **Actions float on major tags** (`checkout@v6`, `setup-python@v6`, `upload-artifact@v5`). Fine
  as-is given `permissions: contents: read`; worth pinning to SHAs only if a publishing workflow
  ever gains `id-token: write`.
- **The sdist omits `CHANGELOG.md`.** It ships `LICENSE`, `NOTICE`, `README.rst`, the package, and
  `tests/`. Low impact, since the `Changelog` project URL is in the metadata.

## 7. Release mechanics

You chose local publishing via `make publish`, so these are the gaps specific to that path:

- **No tag-versus-`__version__` check.** `git tag v0.2.0` and `__version__ = "0.2.0"` are coupled
  only by attention. The clean-tree guard cannot catch a mismatch. A one-line comparison in the
  `publish` recipe would close the last hole in the release process, and it is the item I would
  add first.
- **No provenance attestations.** PEP 740 attestations, and the "Verified details" badge PyPI
  shows for them, are only obtainable through Trusted Publishing from CI. This is the accepted
  cost of publishing locally, recorded here so the tradeoff is not forgotten rather than as a
  recommendation to revisit.

## 8. Documentation nits

- **The scale caveat lives only in the README.** `prefsorted` is
  O(`len(preferred)` × `len(seq)`) via repeated `list.index`/`list.pop`. The README says a few
  dozen items is the intended scale; the docstring does not, and the docstring is what an IDE
  shows.
- **`reverse=True` is a naming trap.** It relocates preferred values to the end while keeping them
  in preference order, rather than reversing anything — different from what `sorted(reverse=True)`
  trains people to expect. Documented behavior, but a sentence contrasting it with `sorted` would
  preempt the misreading.
