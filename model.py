from dataclasses import dataclass


@dataclass
class Ticket:
    id: str
    tags: list[str]
    contents: dict[str, str]
    last_modified: str
    created_at: str

    def as_json(self):
        return {
            "uuid": self.id,
            "tags": self.tags,
            "contents": self.contents,
            "last_modified": self.last_modified,
            "created_at": self.created_at,
        }


sample_entry = {
    "uuid": "198ed5dd-fbc7-42e6-b857-1ad898afsfb3",
    "title": "Easiest task ever",
    "description": "Do stuff",
    "repository": "N/A",
    "skills": "N/A",
    "difficulty": "Dark Souls No Hit",
    "assignee": "idy",
    "roles": ["Critical"],
    "last_modified": "2022-08-23 10:04:09.104992",
    "created_at": "2022-08-20 10:04:09.104992"
}
