from dataclasses import dataclass
from typing import Any


@dataclass
class HTInitVar:
    param: str
    default: Any = None
    init_arg: str = None
    fill_with: str = None
