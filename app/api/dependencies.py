
from . import database, schemas, session_manager
from fastapi.exceptions import HTTPException


def get_db():
    """dependence to acces into de db"""
    db = database.SessionLocal()
    try:
        yield db
    
    finally:
        db.close()

async def user_parameters(user_id: str | None = None, user_name: str | None = None, base_user_body: schemas.SingleUser | None = None, user_body: schemas.UserCreate | None = None):
    return {"user_id": user_id, "user_name": user_name, "base_user_body": base_user_body, "user_body": user_body}

async def item_paramters(item_id: str | None = None, item_body: schemas.ItemCreate | None = None):
    return {"item_id": item_id, "item_body": item_body}

async def books_parameters(book_id: str | None = None, owner_id: str | None = None, book_body: schemas.CreateBook | None = None):
    return {"book_id": book_id, "owner_id": owner_id, "book_body": book_body}

verifier = session_manager.BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=session_manager.backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

# Uses UUID
cookie = session_manager.SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=session_manager.cookie_params,
)