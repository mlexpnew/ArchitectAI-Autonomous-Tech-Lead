from dataclasses import dataclass
from datetime import datetime


@dataclass
class Artifact:

    name: str

    category: str

    author: str

    content: str

    version: int = 1

    created_at: str = datetime.now().isoformat()