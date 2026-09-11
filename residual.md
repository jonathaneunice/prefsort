# Residual review findings

Recommendations from the September 2026 project review that have **not** been acted on.

Closed since the review: the 0.2.0 version bump and changelog entry, the index-based `prefsorted`
fix and its regression test, the full Apache-2.0 `LICENSE` plus `NOTICE`,
`filterwarnings = ["error"]`, the Beta development-status classifier, the removal of
`AUTHORS.rst`, the local `make publish` / `make publish-test` release path, version moved into
`pyproject.toml` and read back through `importlib.metadata`, doctest and README-example
execution, the three missing behavior tests, the retirement of pre-commit in favor of
`make lint`, CI concurrency and timeouts, `CHANGELOG.md` in the sdist, the scale caveat in
the docstring, the `reverse=True` contrast with `sorted`, and the README example test counting
`.. code-block:: python` directives instead of a fixed block count.

Items are ordered by the value-to-effort ratio as I judged it, not by severity. None are release
blockers for 0.2.0.

---

## 1. The string shorthand is still unsound in the type signature

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

**Be aware of the limit before adopting this.** Tested against mypy strict, it does not reject
the bad call outright. In a bare statement, `prefsorted([1, 2, 3], "2")` resolves to
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

This is the only remaining correctness-adjacent item.

## 2. Release mechanics

Publishing is local, via `make publish`. Two gaps specific to that choice:

- **No tag-versus-version check.** `git tag v0.2.0` and `version = "0.2.0"` in `pyproject.toml`
  are coupled only by attention, and the clean-tree guard cannot catch a mismatch. A comparison
  in the `publish` recipe would close the last hole in the release process. Note that this must
  read `pyproject.toml` (or `importlib.metadata` after a reinstall) — there is no longer a
  version constant in the source to compare against.
- **No provenance attestations.** PEP 740 attestations, and the "Verified details" badge PyPI
  shows for them, are only obtainable through Trusted Publishing from CI. This is the accepted
  cost of publishing locally, recorded so the tradeoff is not forgotten rather than as a
  recommendation to revisit.

One related wrinkle worth remembering rather than fixing: because `__version__` now comes from
installed distribution metadata, a version bump is not visible to the running interpreter until
the package is reinstalled. Builds and uploads read `pyproject.toml` directly and are unaffected.

## 3. Non-Python files have no whitespace or end-of-file check

YAML and TOML syntax, `pyproject.toml` schema, and GitHub Actions workflows are now checked by
`make lint` (`check-yaml`, `check-toml`, `validate-pyproject`, `actionlint`). Trailing whitespace
and a missing final newline in Python files are errors via Ruff `W`.

What is still not covered: trailing whitespace and missing final newlines in `README.rst`,
`CHANGELOG.md`, `Makefile`, `MANIFEST.in`, and this file. A small `hygiene` make target over
`git ls-files` could, if it ever proves to matter; for a repo this size it is probably noise.

`actionlint` comes from `actionlint-py`, a pip wrapper that downloads the Go binary at install
time, and it finds `shellcheck` the same way via `shellcheck-py`. `make install` is enough
locally and in CI. There is no local git hook, so lint still runs only when someone types
`make lint` or when CI runs it on a pull request.

## 4. CI hygiene leftovers

- **No Dependabot configuration** for GitHub Actions, so action versions age silently. This is
  the one remaining item from the original CI list that has real upkeep value.
- **Actions float on major tags** (`checkout@v6`, `setup-python@v6`, `upload-artifact@v5`). Fine
  as-is given `permissions: contents: read`; worth pinning to SHAs only if a publishing workflow
  ever gains `id-token: write`.
