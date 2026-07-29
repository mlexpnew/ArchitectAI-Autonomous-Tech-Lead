"""
Entity Definition
"""

from dataclasses import dataclass
from dataclasses import field


@dataclass
class EntityField:

    name: str
    type: str


@dataclass
class Entity:

    name: str

    fields: list[EntityField] = field(default_factory=list)