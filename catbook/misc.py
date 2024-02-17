from configparser import RawConfigParser
from dataclasses import dataclass
from os import path
from typing import Optional, Self


@dataclass
class Misc:
    CONFIG: str = "misc.ini"

    def __post_init__(self):
        self._config = RawConfigParser()
        self._load_config()
        self._section = "misc"
        self._index = 0
        self._name = None

    def __iter__(self) -> Self:
        return self

    def __next__(self):
        if self._name is None:
            raise StopIteration
        val = self.get(f"{self._name}_{self._index}")
        if val is None:
            self._index = 0
            self._name = None
            raise StopIteration
        else:
            self._index = self._index + 1
            return val

    def get_numbered(self, name: str) -> Self:
        """use as: values = [ _ for _ in misc.get_numbered("email")]"""
        self._name = name
        self._index = 0
        return self

    def get(self, name: str) -> Optional[str]:
        return self._config.get(self._section, name, fallback=None)

    def reload(self) -> None:
        self._load_config()

    def _load_config(self) -> None:
        if path.isfile(self.CONFIG):
            self._config.read(self.CONFIG)
        else:
            print(f"No misc {self.CONFIG} file found.")
