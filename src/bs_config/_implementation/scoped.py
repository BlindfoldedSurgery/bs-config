from collections.abc import Callable
from datetime import date, datetime, time

from bs_config import Env


class ScopedEnv(Env):
    def __init__(self, parent: Env, prefix: str) -> None:
        if not prefix:
            raise ValueError("scope key cannot be empty")
        self.__parent = parent
        self.__prefix = prefix

    def __truediv__(self, key: str, /) -> Env:
        if not key:
            raise ValueError("Key cannot be empty")

        return ScopedEnv(self, key)

    def get_string[T = str](  # type: ignore[override]
        self,
        key: str,
        *,
        default: T | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> T | None:
        return self.__parent.get_string(
            f"{self.__prefix}.{key}",
            default=default,
            required=required,
            transform=transform,
        )

    def get_bool(  # type: ignore[override]
        self,
        key: str,
        *,
        default: bool,
    ) -> bool:
        return self.__parent.get_bool(
            f"{self.__prefix}.{key}",
            default=default,
        )

    def get_int(  # type: ignore[override]
        self,
        key: str,
        *,
        default: int | None = None,
        required: bool = False,
    ) -> int | None:
        return self.__parent.get_int(
            f"{self.__prefix}.{key}",
            default=default,  # type: ignore[arg-type]
            required=required,
        )

    def get_string_list[T = str](  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[T] | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> list[T] | None:
        return self.__parent.get_string_list(
            f"{self.__prefix}.{key}",
            default=default,  # type: ignore[arg-type]
            required=required,
            transform=transform,
        )

    def get_int_list(  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[int] | None = None,
        required: bool = False,
    ) -> list[int] | None:
        return self.__parent.get_int_list(
            f"{self.__prefix}.{key}",
            default=default,  # type: ignore[arg-type]
            required=required,
        )

    def get_datetime(  # type: ignore[override]
        self,
        key: str,
        *,
        default: datetime | None = None,
        required: bool = False,
        is_naive: bool = False,
    ) -> datetime | None:
        return self.__parent.get_datetime(
            f"{self.__prefix}.{key}",
            default=default,  # type: ignore[arg-type]
            required=required,
            is_naive=is_naive,
        )

    def get_date(  # type: ignore[override]
        self,
        key: str,
        *,
        default: date | None = None,
        required: bool = False,
    ) -> date | None:
        return self.__parent.get_date(
            f"{self.__prefix}.{key}",
            default=default,  # type: ignore[arg-type]
            required=required,
        )

    def get_time(  # type: ignore[override]
        self,
        key: str,
        *,
        default: time | None = None,
        required: bool = False,
    ) -> time | None:
        return self.__parent.get_time(
            f"{self.__prefix}.{key}",
            default=default,  # type: ignore[arg-type]
            required=required,
        )
