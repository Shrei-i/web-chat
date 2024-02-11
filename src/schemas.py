from datetime import datetime

from pydantic import BaseModel



class Chat(BaseModel):
    chat_id: int
    chat_name: str
    user_id: int

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    user_id: int
    content: str
    date_create: datetime
class Message(MessageBase):
    message_id: int
    chat_id: int


    class Config:
        from_attributes = True #при создании экземпляра модели данные будут браться из атрибутов объекта Python, а не из словаря

class UserBase(BaseModel):
    id: int
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Party(BaseModel):
    user_id: int
    chat_id: int