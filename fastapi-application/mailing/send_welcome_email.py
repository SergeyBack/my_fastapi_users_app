from core.models import User, db_helper
from crud import users

from .send_email import send_email

async def send_welcome_email(user_id: int) ->None:
    async with db_helper.session_factory() as session:
        user: User | None= await users.get_user(
            session=session,
            user_id=user_id,
        )
    
    if user:
        await send_email(
            recipient=user.email,
            subject="Welcome to our site!",
            body = f"Dear {user.email}, \n\nYou succesfully registered",
    )