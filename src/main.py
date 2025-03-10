import fastapi.middleware
import fastapi.middleware
import fastapi.middleware.cors
from sqladmin import Admin

from src.api.friend.api import friend_router
from src.api.hello import router as hello_world
from src.api.user.api import auth_router, users_router
import config
import fastapi_mail
from src.auth.api import views as auth_views
from src.user import admin
from src.user.api import views as user_views

app = fastapi.FastAPI()
admin_core = Admin(app, engine=config.engine)
admin_core.add_view(admin.UserAdmin)

@app.get("/aboba")
async def send_email():
    message = fastapi_mail.MessageSchema(
        subject="Test email sending message",
        recipients=["test@mail.ru"],
        body="""
            <p>Thanks for using Fastapi-mail</p>
        """,
        subtype=fastapi_mail.MessageType.html,
    )
    fm = fastapi_mail.FastMail(config.email_config)
    await fm.send_message(message)

    return {"status": "Ready"}

app.include_router(auth_views.auth_router)
app.include_router(user_views.user_router)

app.include_router(friend_router)

allows_origins = [
    "http://localhost:4200",
    "http://localhost:8080",
    "https://tetris-game.ru",
]

app.add_middleware(
    middleware_class=fastapi.middleware.cors.CORSMiddleware,
    allow_origins=allows_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
