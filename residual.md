# Residual review findings

Recommendations from the September 2026 project review that have **not** been acted on.

Closed since the review: the 0.2.0 version bump and changelog entry, the index-based `prefsorted`
fix and its regression test, the full Apache-2.0 `LICENSE` plus `NOTICE`,
`filterwarnings = ["error"]`, the Beta development-status classifier, the removal of
`AUTHORS.rst`, the local `make publish` / `make publish-test` release path, version moved into
`pyproject.toml` and read back through `importlib.metadata`, doctest and README-example
execution, the three missing behavior tests, the retirement of pre-commit in favor of
`make lint`, CI concurrency and timeouts, `CHANGELOG.md` in the sdist, the scale caveat in
the docstring, the `reverse=True` contrast with `sorted`, the README example test counting
code fences instead of a fixed block count, the switch of the landing README from RST to Markdown,
Dependabot for GitHub Actions, the string-shorthand docstring caveat, and non-Python
whitespace left as constitution policy rather than a checker.

Items are ordered by the value-to-effort ratio as I judged it, not by severity. None are release
blockers for 0.2.0.

---

## Rejected: overloads for the string shorthand

`preferred: str | Iterable[T] | None` looks unsound because
`prefsorted([1, 2, 3], "2")` type-checks and does nothing. That call is a category error, not a
hole in the types. A string *preferred* is split, then compared with `==`. Missing preferences
are ignored, so the call searches for the string `"2"`, not the integer `2` — the same rule as
`prefsorted([1, 2, 3], [4])`.

Overloads that allow `str` only when *seq* is `Iterable[str]` encode a usage convention as if it
were the contract. At runtime a string *preferred* is legal for any `T`, including mixed sequences
where a token really matches. The overloads still accept the “bad” call as `list[object]` until
the result is annotated, and a complete coupling of shorthand to string items is not expressible
without giving up generator `preferred`. Do not add them. The docstring states the failure mode.

## 1. Release mechanics

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

## 2. CI hygiene leftovers

- **Actions float on major tags** (`checkout@v6`, `setup-python@v6`, `upload-artifact@v6`). Fine
  as-is given `permissions: contents: read`; worth pinning to SHAs only if a publishing workflow
  ever gains `id-token: write`. Dependabot will open PRs for new majors.
