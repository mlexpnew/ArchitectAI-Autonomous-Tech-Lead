from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentMessage:

    sender: str

    receiver: str

    title: str

    content: str

    timestamp: datetime = datetime.now()