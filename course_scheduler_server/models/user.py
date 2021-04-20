from typing import Optional


# User class

class User:
    id: str
    email: Optional[str]
    name: Optional[str]
    picture: Optional[str]

    def __init__(self, uid: str, email: Optional[str], name: Optional[str], picture: Optional[str]) -> None:
        self.id = uid
        self.email = email
        self.name = name
        self.picture = picture

    def to_db_dict(self):
        return {
            "_id": self.id,
            "email": self.email,
            "name": self.name,
            "picture": self.picture
        }
