from datetime import datetime

from sqlalchemy import Integer, Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship('Chat', secondary='party', back_populates='user', cascade="all, delete")
    message = relationship('Message', back_populates='user',cascade="all, delete")

class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True, unique=True)
    chat_name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))  # пользователь, создавший чат
    user = relationship('User', secondary='party', back_populates='chat')
    message = relationship('Message', back_populates='chat')


class Party(Base):
    __tablename__ = 'party'
    chat_id = Column(Integer, ForeignKey('chats.chat_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    date_create = Column(DateTime, default=datetime.utcnow)

    user = relationship('User')
    chat = relationship('Chat')
