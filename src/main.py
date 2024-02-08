from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.database import SessionLocal, engine
from fastapi.responses import HTMLResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency для автоматического закрытия сессии бд при завершении функций
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users/', response_model=schemas.User)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, id=user.id)
    if db_user:
        raise HTTPException(400,'Такой id уже занят')
    else:
        return crud.create_user(db, user)

@app.post('/chats/', response_model=schemas.Chat)
def create_chat(chat:schemas.Chat, db:Session = Depends(get_db)):
    db_chat = crud.get_chat(db, id=chat.chat_id)
    if db_chat:
        raise HTTPException(400, 'Чат с таким id существует, придумайте другой')
    else:
        return crud.create_chat(db, chat)
@app.post('/chats/{chat_id}/{user_id}/message', response_model=schemas.Message)
def send_message(chat_id: int, user_id: int, text:str, db:Session = Depends(get_db)):
    in_party = crud.get_party(db,chat_id,user_id)
    if in_party:
        return crud.new_message(db, user_id, chat_id, text)
    else:
        raise HTTPException(400, 'Отказано в доступе')

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id:int, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, id = user_id)
    if db_user:
        return db_user
    else:
        raise HTTPException(404, 'Пользователь не найден')








# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <h2>Your ID: <span id="ws-id"></span></h2>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var client_id = Date.now()
#             document.querySelector("#ws-id").textContent = client_id;
#             var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """
#
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []
#
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#
#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)
#
#
#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)
#
#
# manager = ConnectionManager()
#
#
# @app.get("/")
# async def get():
#     return HTMLResponse(html)
#
#
# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")