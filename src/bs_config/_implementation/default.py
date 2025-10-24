from collections.abc import Callable

from bs_config import Env

from .scoped import ScopedEnv


class DefaultEnv(Env):
    def __init(self) -> None:
        pass

    def __truediv__(self, key: str, /) -> Env:
        return ScopedEnv(self, key)

    def get_string[T = str](  # type: ignore[override]
        self,
        key: str,
        *,
        default: T | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> T | None:
        if required and default is None:
            raise ValueError(f"Missing config value for {key}")

        return default

    def get_bool(  # type: ignore[override]
        self,
        key: str,
        *,
        default: bool,
    ) -> bool:
        return default

    def get_int(  # type: ignore[override]
        self,
        key: str,
        *,
        default: int | None = None,
        required: bool = False,
    ) -> int | None:
        if default is None and required:
            raise ValueError(f"Missing config value for {key}")

        return default

    def get_string_list[T = str](  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[T] | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> list[T] | None:
        if default is None and required:
            raise ValueError(f"Missing config value for {key}")

        return default

    def get_int_list(  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[int] | None = None,
        required: bool = False,
    ) -> list[int] | None:
        if default is None and required:
            raise ValueError(f"Missing config value for {key}")

        return default
