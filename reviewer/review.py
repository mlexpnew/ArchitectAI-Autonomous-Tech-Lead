"""
Review Result
"""

from dataclasses import dataclass


@dataclass
class Review:
    passed: bool
    score: int
    feedback: str