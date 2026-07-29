from dataclasses import dataclass


@dataclass
class Relationship:

    source: str

    target: str

    relationship_type: str

    foreign_key: str