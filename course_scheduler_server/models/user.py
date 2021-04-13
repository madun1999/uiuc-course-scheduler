from typing import ByteString


# User class

class User:
    id : str
    email : str

    def __init__(self, id : str, email : str) -> None:
        self.id = id
        self.email = email
    
    def to_db_dict(self):
        return {"_id": self.id, "email": self.email}

