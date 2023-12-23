#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, WebSocket, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import PlainTextResponse, FileResponse, RedirectResponse, JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from api import crud, models, encrypt, dependencies, schemas, json_encoder, session_manager
from typing import Annotated
from api.database import engine, inspector
import sys, os, json
import uvicorn
from uuid import UUID, uuid4

app = FastAPI(
    debug=True,
    title="Login and Register API",
    summary = "This is a login/register application created by Pau Mateu ",
    docs_url= "/documentation",
    description="This will nothing :D",
    version="0.12.3"
)

Key = encrypt.EncryptPassword.read_key()
Encrypter = encrypt.EncryptPassword(Key)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You might want to specify exact origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", description = "This is the main function that will be redirected to show_tables_name")
def main():
    return RedirectResponse(url="/show_tables_name")


@app.get("/get_user/{user_id}")
def get_user_by_id(user_params: Annotated[dict, Depends(dependencies.user_parameters)], db: Session = Depends(dependencies.get_db)):
    try:
        return {"Result": crud.get_user(db=db, user_id=user_params['user_id'])}
    except:
        return {"Error": f"User {user_params['user_id']} doesn't exist."}


@app.get("/show_tables_name", description="Get all the current tables from the database")
def show_tables():
    table_names = inspector.get_table_names()
    return {"Table_Names":table_names}


@app.get("/show_users_table", description="Show all conent of users table")
def show_user_table():
    with engine.connect() as conn:
        result = conn.execute(crud.select(models.Users))
        users = result.scalars().all()

    return users


@app.get("/get_all_users", description="Get all the users from users table")
async def get_all_users(db: Session = Depends(dependencies.get_db)):
    result = crud.get_users(db=db, limit=999)
    return {"response":result}


@app.get("/get_item/{item_id}", description="Get and item from item table")
async def get_an_item(item_params: Annotated[dict, Depends(dependencies.item_paramters)], db: Session = Depends(dependencies.get_db)):
    result = crud.get_item(db=db, item_id=item_params['item_id'])
    return {"response":result}


@app.post("/post_user", description="Add a new user into to User table")
async def post_user(user_body: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    # In this function there are an error when we create another consecutive user, solve it.
    try:
        db_user = crud.get_user_by_email(db, email=user_body.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        return {"response": crud.create_user(db=db, user=user_body)}
        

    except Exception.IntegrityError:
        raise HTTPException(status_code=400, detail="Duplicate item ID or other integrity error")   

    except Exception as e:
        return {"error": f"an error ocurred: {e}"}


@app.post("/post_item", description="Post new item into item table")
async def post_item(item_params: Annotated[dict, Depends(dependencies.item_paramters)], db: Session = Depends(dependencies.get_db)):
    try:
        user = crud.get_user(db, str(item_params['item_body'].owner_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"response": crud.create_item(db=db, item=item_params['item_body'])}

    except Exception as e:
        return{"error": f"an error ocurred: {e}"}


@app.put("/update_user/{user_id}", description="Update an user from the users table")
async def update_user(user_params: Annotated[dict, Depends(dependencies.user_parameters)], db: Session = Depends(dependencies.get_db)):
    try:
        if not user_params['user_id']:
            raise HTTPException(status_code=404, detail="Invalid input (PUT /update_user/<user_id>)")
        
        return {"Response": crud.update_user(db=db, user_id=user_params['user_id'], user=user_params['user_body'])}

    except Exception as e:
        return {"error": f"an error ocurred: {e}"}


@app.put("/update_item/{item_id}", description="Updatea single item from items table")
async def update_item(item_params: Annotated[dict, Depends(dependencies.item_paramters)], db: Session = Depends(dependencies.get_db)):
    try:
        if not item_params['item_id']:
            raise HTTPException(status_code=404, detail="Invalid input (PUT /update_item/<item_id>)")
        
        return {"Response": crud.update_item(db=db, item_id=item_params['item_id'], item=item_params['item_body'])}

    except Exception as e:
        return {"error":f"an error ocurred: {e}"}


@app.delete("/delete_user/{user_id}", description="Delete an user from the user table")
async def delete_user(user_params: Annotated[dict, Depends(dependencies.user_parameters)], db: Session = Depends(dependencies.get_db)):
    # Change note deleted
    try:
        if not user_params['user_id']:
            raise HTTPException(status_code=404, detail="Invalid input (DELETE /delete_user<user_id>)")

        return {"Response": crud.delete_user(db=db, user_id=user_params['user_id'])}
    
    except Exception as e:
        return {"error": f"an error ocurred: {e}"}


@app.delete("/delete_item/{item_id}", description="Delete an item from the item table")
async def delet_item(item_params: Annotated[dict, Depends(dependencies.item_paramters)], db: Session = Depends(dependencies.get_db)):
    try:
        if not item_params['item_id']:
            raise HTTPException(status_code=404, detail="Invalid input (DELETE /delete_item/<item_id>)")

        
        return {"Response": crud.delete_item(db=db, item_id=item_params['item_id'])}
    
    except Exception as e:
        return {"error": f"an error ocurred: {e}"}


@app.post("/check_user", description="Check if user exists in the users table")
async def check_if_user(user_params: Annotated[dict, Depends(dependencies.user_parameters)], db: Session = Depends(dependencies.get_db)):
    try:
        if not user_params['base_user_body'].username or not user_params['base_user_body'].password:
            raise HTTPException(status_code=404, detail="Invalid input (GET /check_user/<user_name>/<hashed_password>)")

        # Check if username matches with the user table
        username = db.query(models.Users).filter(models.Users.username == user_params['base_user_body'].username).first()
        if not username:
            return {"result": False, "Message": f"Username {user_params['base_user_body'].username} doesn't exists!"}

        # In case username exists into the table, check the password
        Decrypted_Password = Encrypter.decrypt_password(bytes(username.hashed_password))

        if Decrypted_Password == user_params['base_user_body'].password:
            return {"result":True, "Message":f"Logged successfully as {user_params['base_user_body'].username}"}
        return {"result":False, "Message":"Incorrect password!"}      
        
    except Exception as e:
        return {"error": f"an error ocurred: {e}"}


@app.get("/get_password/{username}", description="Get hashed password by its username from user table")
async def get_user_password(username: str, db: Session = Depends(dependencies.get_db)):
    try:
        if not username:
            raise HTTPException(status_code=404, detail="Invalid input (GET /get_password/<username>)")

        crypted_password = crud.fetch_user_password(db=db, username=username)

        decrypted_password = Encrypter.decrypt_password(crypted_password)
        
        return {"password": decrypted_password}
    
    except Exception as e:
        return {"error": f"an error ocurred: {e}"}

# --------------------Second part of my API----------------------------------------

@app.get("/get_books_by_owner_id/{owner_id}", description="Get all books by its owner_id, this also uses a json encoder")
async def get_books_by_owner_id(books_params: Annotated[dict, Depends(dependencies.books_parameters)], db: Session = Depends(dependencies.get_db)):
    try:
        if not books_params['owner_id']:
            raise HTTPException(status_code=404, detail="Invalid input (GET /get_books_by_owner_id/<owner_id>)")

        books = crud.get_books_by_author(db=db, owner_id=books_params['owner_id'])
        
        books_list = []
        for result in books:
            book_data = crud.get_books_by_id(db=db, book_id=result[0])
            books_list.append(jsonable_encoder(book_data))
        
        response_data = {"result": books_list}
        json_str = json.dumps(response_data, cls=json_encoder.LargeFloatEncoder)
        return JSONResponse(content=json_str)
    except Exception as e:
        response_data = {"an error ocurred": e}
        json_str = json.dumps(response_data, cls=json_encoder.LargeFloatEncoder)
        return JSONResponse(content=json_str)
    

@app.post("/create_book/{owner_id}", description="create a new book")
async def create_book(books_params: Annotated[dict, Depends(dependencies.books_parameters)], db: Session = Depends(dependencies.get_db)):
    """revise this fucntion because i've done this on my class"""
    try:
        if not books_params['owner_id']:
            raise HTTPException(status_code=404, detail="*change this*", headers=["",""])
    
        return {"result":  crud.create_book(db=db, book=books_params['book_body'], owner_id=books_params['owner_id'])}
    
    except Exception as e:
        return {"error": f"An error ocurred: {e}"}

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.get("/getimage/{image_name}")
async def get_image(image_name: str):
    image_path = f"images/{image_name}"
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/png")
    print("Image not found!")  # Debugging line
    return {"error": f"Image {image_name} not found"}


# ------------------------------------------------ Web Socket Part --------------------------------------------

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/web_socket_test")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()


        await websocket.send_text(f"Message text was: {data} - {len(data)}")

# ----- Sessions ----
@app.post("/create_session/{name}")
async def create_session(name: str, response: Response):

    session = uuid4()
    data = session_manager.SessionData(username=name)

    await session_manager.backend.create(session, data)
    dependencies.cookie.attach_to_response(response, session)

    return f"created session for {name}"


@app.get("/whoami", dependencies=[Depends(dependencies.cookie)])
async def whoami(session_data: session_manager.SessionData = Depends(dependencies.verifier)):
    return session_data


@app.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(dependencies.cookie)):
    await session_manager.backend.delete(session_id)
    dependencies.cookie.delete_from_response(response)
    return "deleted session"
        
        
if __name__ == "__main__":
    uvicorn.run(
        "app:main",
        host="127.0.0.1",
        port = 800,
        reload=True
    )