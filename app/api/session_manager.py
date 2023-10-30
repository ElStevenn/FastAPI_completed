# session_manager.py
from fastapi.security.sessions import Session
from fastapi import Depends

async def get_current_user(session_data: dict = Depends(Session.get_session)):
    username = session_data.get("username")
    if not username:
        return None
    return username

def init_sessions(app):
    app.add_middleware(Session, secret_key="your_secret_key", session_cookie="session", max_age=3600)
