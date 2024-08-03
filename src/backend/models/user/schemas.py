from models.base_schema import BaseModel, ConfigDict

class User(BaseModel):
    user_id: int | None = None
    username: str
    email: str
    active: bool | None = None

class UserCreate(User):
    model_config = ConfigDict(from_attributes=True)

    hashed_password: str
