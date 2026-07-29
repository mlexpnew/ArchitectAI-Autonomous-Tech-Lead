"""
Shared Artifact
"""

from dataclasses import dataclass


@dataclass
class Artifact:

    name: str

    category: str

    author: str

    content: str

    version: int = 1