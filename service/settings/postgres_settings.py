from dataclasses import dataclass
from typing import Any


@dataclass
class PostgresSettings:
    host: str
    port: str
    username: str
    password: str
    db_name: str
    declarative_base: Any = None
