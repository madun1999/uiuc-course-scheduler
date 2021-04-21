from typing import Optional, TypedDict


class User(TypedDict):
    id: str
    email: Optional[str]
    name: Optional[str]
    picture: Optional[str]


def make_user(*_, uid: str, email: Optional[str], name: Optional[str], picture: Optional[str]) -> User:
    return User(
        id=uid,
        email=email,
        name=name,
        picture=picture,
    )


def user_to_db_dict(user: User):
    return {
        "_id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "picture": user["picture"]
    }
