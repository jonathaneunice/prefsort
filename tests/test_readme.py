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
    n_directives = sum(
        1 for line in README.read_text().splitlines() if line.strip() == ".. code-block:: python"
    )
    blocks = readme_python_blocks()

    assert n_directives
    assert len(blocks) == n_directives

    namespace: dict[str, Any] = {"df": _FakeFrame()}
    for block in blocks:
        exec(block, namespace)
