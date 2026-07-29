"""
Project Blueprint

Contains all information required to generate
a complete backend project.
"""

from dataclasses import dataclass

from generators.entities.entity import Entity
from generators.entities.relationship import Relationship


@dataclass
class ProjectBlueprint:

    name: str

    entities: list[Entity]

    relationships: list[Relationship]