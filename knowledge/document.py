"""
Project Document
"""

from dataclasses import dataclass


@dataclass
class ProjectDocument:

    path: str

    content: str

    embedding: list[float] | None = None