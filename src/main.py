from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency для автоматического закрытия сессии бд при завершении функций
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users/', response_model=schemas.User) #создание пользователя
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, id=user.id)
    if db_user:
        raise HTTPException(400,'Такой id уже занят')
    else:
        return crud.create_user(db, user)

@app.post('/chats/', response_model=schemas.Chat) #создание чата
def create_chat(chat:schemas.Chat, db:Session = Depends(get_db)):
    db_chat = crud.get_chat(db, chat_id=chat.chat_id)
    if db_chat:
        raise HTTPException(400, 'Чат с таким id существует, придумайте другой')
    else:
        return crud.create_chat(db, chat)
@app.post('/chats/{chat_id}/{user_id}/message') #отправка сообщения пользователя в конкретный чат
def send_message(chat_id: int, user_id: int, text:str, db:Session = Depends(get_db)):
    party = crud.get_party_chat(db, chat_id)
    if user_id in [i.user_id for i in party]:
        return crud.new_message(db, user_id, chat_id, text)
    else:
        raise HTTPException(400, 'Отказано в доступе')

@app.get("/users/{user_id}", response_model=schemas.User) #поиск пользователя по id
def read_user(user_id:int, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, id = user_id)
    if db_user:
        return db_user
    else:
        raise HTTPException(404, 'Пользователь не найден')

@app.get("/chats/{chat_id}", response_model=schemas.Chat) #поиск чата по id
def read_chat(chat_id:int, db: Session = Depends(get_db)):
    db_chat = crud.get_chat(db, chat_id)
    if db_chat:
        return db_chat
    else:
        raise HTTPException(404, 'Чат не найден')

@app.get("/users/find/{username}", response_model=list[schemas.User]) #поиск пользователей по никнеймам
def get_username(username:str, db: Session = Depends(get_db)):
    users = crud.get_username(db, username)
    if users:
        return users
    else:
        raise HTTPException(404, 'Ни одного пользователя не найдео')

@app.get("/chat_users/{chat_id}", response_model=[]) #показывает пользователей состоящих в данном чате
def get_chat_users(chat_id:int, db:Session = Depends(get_db)):
    party = crud.get_party_chat(db, chat_id)
    return [i.user_id for i in party]
    # else:
    #     raise HTTPException(404, 'Ни одного пользователя не найдео')


@app.get("/user_chats/{user_id}", response_model=[]) #показывает список чатов в которых состоит конкретный пользователь
def get_party(user_id:int, db:Session = Depends(get_db)):
    party = crud.get_party_user(db, user_id)
    return [i.chat_id for i in party]

@app.get("/chats/{chat_id}/messages", response_model=list[schemas.MessageBase])
def get_messages(chat_id:int, db:Session = Depends(get_db)):
    messages = crud.get_messages(db, chat_id)
    return messages


@app.put("/user/update/{user_id}", response_model=schemas.User) #обновление имени и пароля пользователя
def update_user(user_id:int, new_username:str = None, new_password:str = None, db:Session = Depends(get_db)):
    return crud.update_user(db, user_id, new_username, new_password)



@app.put("/chats/add_user/{chat_id}", response_model=schemas.Party)
def update_chat(user_id: int, chat_id:int, db:Session = Depends(get_db)):
    return crud.update_chat(db, chat_id, user_id)


@app.delete("/user/del/{user_id}")
def delete_user(user_id:int, db:Session = Depends(get_db)):
    return crud.delete_user(db, user_id)