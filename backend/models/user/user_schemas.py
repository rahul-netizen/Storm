from pydantic import BaseModel

class User(BaseModel):
    user_id: int | None = None
    username: str
    email: str
    active: bool | None = None

class UserCreate(User):
    hashed_password: str
    class config:
        orm_mode = True
