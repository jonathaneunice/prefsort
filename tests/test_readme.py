"""
Execute the Python examples embedded in README.md.
"""

import re
from pathlib import Path
from typing import Any, ClassVar

README = Path(__file__).parent.parent / "README.md"

# Opening fences of the form ```python, not ```console or other languages.
PYTHON_FENCE = re.compile(r"^```python[ \t]*$", re.MULTILINE)
PYTHON_BLOCK = re.compile(r"^```python[ \t]*\n(.*?)```", re.MULTILINE | re.DOTALL)


class _FakeFrame:
    """
    Stand-in for the DataFrame in the column-ordering example.
    """

    columns: ClassVar[list[str]] = ["name", "size", "id"]

    def reindex(self, columns: list[str]) -> list[str]:
        return columns


def readme_python_blocks() -> list[str]:
    return [match.group(1) for match in PYTHON_BLOCK.finditer(README.read_text())]


def test_readme_examples_execute() -> None:
    n_fences = len(PYTHON_FENCE.findall(README.read_text()))
    blocks = readme_python_blocks()

    assert n_fences
    assert len(blocks) == n_fences

    namespace: dict[str, Any] = {"df": _FakeFrame()}
    for block in blocks:
        exec(block, namespace)
