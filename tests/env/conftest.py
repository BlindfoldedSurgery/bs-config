from collections.abc import Callable
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def example_file_loader() -> Callable[[str], Path]:
    data_dir = Path(__file__).with_name("data")

    def __load(name: str) -> Path:
        result = data_dir / name
        if not result.is_file():
            raise RuntimeError(f"Example file {result} does not exist")

        return result

    return __load
