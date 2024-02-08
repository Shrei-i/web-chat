from sqlalchemy.orm import Session
from . import models, schemas

#create операции
def create_user(db:Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, username=user.username)
    db.add(db_user) #добавление нового объекта
    db.commit() #фиксация изменений
    db.refresh(db_user) #обновление состояния объекта
    return db_user

def create_chat(db: Session, chat: schemas.Chat):
    db_chat = models.Chat(chat_name=chat.chat_name, user_id=chat.user_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def new_message(db:Session,user_id:int, chat_id:int, text:str):
    db_message = models.Message(chat_id=chat_id, user_id=user_id, content=text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


#read операции
def get_user(db:Session, id: int): #поиск по id
    return db.query(models.User).filter(models.User.id == id).first()

def get_username(db:Session, username:str): #поиск по никнейму
    return db.query(models.User).filter(models.User.username==username).all()

def get_chat(db:Session, id: int): #все чаты в которых состоит пользователь
    return db.query(models.User).filter(models.User.id == id).first().chat

def get_messages(db:Session, chat_id:int): #сообщения в конкретном чате
    return db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first().message

def get_chat_users(db:Session, chat_id:int): #пользователи состоящие в чате
    return db.query(models.Chat).filter(models.Chat.chat_id==chat_id).first().user

def get_party(db:Session, chat_id:int, user_id:int):
    return db.query(models.Party).filter_by(user_id=user_id, chat_id=chat_id).first()
#update опереции
def update_user(db:Session, user_id: int, new_usrname:str = None, new_password: str=None):
    person = get_user(db, user_id)
    if new_usrname:
        person.username = new_usrname
    if new_password:
        person.hashed_password = new_password + 'notreallyhashed'

    db.commit()
    db.refresh(person)
    return person



def update_chat():
    pass

def update_message():
    pass

#delete операции
def delete_user(db:Session, user_id:int):
    person = db.query(models.User).filter(models.User.id==user_id).first()
    db.delete(person)
    db.commit()
    return person

def delete_chat(db:Session, chat_id:int):
    chat = db.query(models.Chat).filter(models.Chat.chat_id==chat_id).first()
    db.delete(chat)
    db.commit()
    return chat.chat_name



