from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4
import json


@dataclass
class Ticket:
    """
    A class to store ticket attributes.
    :param id: A UUID string
    :type id: str
    :param tags: A list of ticket tags
    :type tags: list[str]
    :param contents: The contents of the ticket(as a JSON)
    :type contents: dict[str, str]
    :param last_modified_at: The time at which the ticket was last modified(as a string)
    :type last_modified_at: str
    :param time_of_creation: The time at which the ticket was created(as a string)
    :type time_of_creation: str
    """

    id: str
    tags: list[str]
    contents: dict[str, str]
    last_modified_at: str
    time_of_creation: str

    def as_json(self):
        return {
            self.id: {
                "tags": self.tags,
                "contents": self.contents,
                "last_modified_at": str(datetime.utcnow()),
                "time_of_creation": self.time_of_creation,
            }
        }