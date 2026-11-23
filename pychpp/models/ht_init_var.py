"""Dataclass describing a request parameter of a model."""

from dataclasses import dataclass
from typing import Any


@dataclass
class HTInitVar:
    """Descriptor for a request parameter of a CHPP xml file.

    Args:
        param: Name of the parameter in the CHPP request.
        default: Default value used when the argument is not given.
        init_arg: Name of the init argument.
        fill_with: Name of the attribute filled with the value.

    """
    param: str
    default: Any = None
    init_arg: str = None
    fill_with: str = None
