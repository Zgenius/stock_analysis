from functools import wraps
from manager.session_manager import SessionManager

def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with SessionManager.get_session() as session:
            return func(*args, session = session, **kwargs)

    return wrapper