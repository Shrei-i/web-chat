from datetime import datetime

from pydantic import BaseModel



class Chat(BaseModel):
    chat_id: int
    chat_name: str
    user_id: int

    class Config:
        orm_mode = True

class Message(BaseModel):
    message_id: int
    chat_id: int
    user_id: int
    content: str
    date_create: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    chats: list[Chat] = []

    class Config:
        orm_mode = True