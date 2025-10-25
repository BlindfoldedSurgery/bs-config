from collections.abc import Callable
from datetime import date, datetime, time

from bs_config import Env


class DefaultEnv(Env):
    def __init(self) -> None:
        pass

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

    def get_datetime(  # type: ignore[override]
        self,
        key: str,
        *,
        default: datetime | None = None,
        required: bool = False,
        is_naive: bool = False,
    ) -> datetime | None:
        if default is None and required:
            raise ValueError(f"Missing config value for {key}")

        if default is not None and ((default.tzinfo is None) != is_naive):
            raise ValueError(
                f"Default value timezone-awareness not as expected for key {key}"
            )

        return default

    def get_date(  # type: ignore[override]
        self,
        key: str,
        *,
        default: date | None = None,
        required: bool = False,
    ) -> date | None:
        if default is None and required:
            raise ValueError(f"Missing config value for {key}")

        return default

    def get_time(  # type: ignore[override]
        self,
        key: str,
        *,
        default: time | None = None,
        required: bool = False,
    ) -> time | None:
        if default is None and required:
            raise ValueError(f"Missing config value for {key}")

        if default is not None and default.tzinfo is not None:
            raise ValueError(f"Default value is timezone-aware for {key}")

        return default
