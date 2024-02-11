from sqlalchemy.orm import Session
from src import models, schemas

#create операции
def create_user(db:Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = models.User(id=user.id, hashed_password=fake_hashed_password, username=user.username)
    db.add(db_user) #добавление нового объекта
    db.commit() #фиксация изменений
    db.refresh(db_user) #обновление состояния объекта

    return db_user

def create_chat(db: Session, chat: schemas.Chat):
    db_chat = models.Chat(chat_name=chat.chat_name, user_id=chat.user_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    #
    db_party = models.Party(user_id=db_chat.user_id, chat_id=db_chat.chat_id)
    db.add(db_party)
    db.commit()
    db.refresh(db_party)
    return db_chat

def new_message(db:Session,user_id:int, chat_id:int, text:str):
    db_message = models.Message(chat_id=chat_id, user_id=user_id, content=text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


#read операции
def get_user(db:Session, id: int): #поиск по id
    user = db.query(models.User).filter(models.User.id == id).first()

    return user

def get_username(db:Session, username:str): #поиск по никнейму
    return db.query(models.User).filter(models.User.username==username).all()

def get_chat(db:Session, chat_id: int):
    return db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first()

def get_messages(db:Session, chat_id:int): #сообщения в конкретном чате
    return db.query(models.Message).filter(models.Message.chat_id == chat_id).all()

def get_party_user(db:Session, user_id:int):
    return db.query(models.Party).filter(models.Party.user_id == user_id).all()

def get_party_chat(db:Session, chat_id:int):
    return db.query(models.Party).filter(models.Party.chat_id == chat_id).all()

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



def update_chat(db:Session, chat_id:int, new_user_id:int):
    party = models.Party(user_id=new_user_id, chat_id=chat_id)
    db.add(party)
    db.commit()
    db.refresh(party)
    return party

def update_message():
    pass

#delete операции

def delete_user_from_chat(db:Session, user_id:int, chat_id:int):
    pass
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



