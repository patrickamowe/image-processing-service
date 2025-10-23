from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserSchema(BaseModel):
    username: str
    password: str

class GetUser(BaseModel):
    user_id: int
    username: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    # tells Pydantic how to read SQLAlchemy objects directly
    model_config = ConfigDict(from_attributes=True)

