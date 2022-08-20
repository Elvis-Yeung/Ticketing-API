from dataclasses import dataclass

@dataclass
class Ticket:
    uuid: str | None
    title: str
    description: str
    repo: str
    difficulty: str
    assignee: str
    role: str
    time: str
    
