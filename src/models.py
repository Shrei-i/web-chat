from datetime import datetime

from sqlalchemy import Integer, Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True) #значения не могут повторяться
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship('Chat', secondary='party', back_populates='user')


class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True)
    chat_name = Column(String)

    user = relationship('User',secondary='party', back_populates='chat' ) #пользователь, создавший чат



class Party(Base):
    __tablename__ = 'party'
    chat_id = Column(Integer, ForeignKey('chats.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    date_create = Column(DateTime, default=datetime.utcnow)

    user = relationship('User')
    chat = relationship('Chat')

