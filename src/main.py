import fastapi
import fastapi.middleware
import fastapi.middleware.cors
from sqladmin import Admin

import config
from src.auth.api import views as auth_views
from src.user import admin
from src.user.api import views as user_views

app = fastapi.FastAPI()
admin_core = Admin(app, engine=config.engine)
admin_core.add_view(admin.UserAdmin)


app.include_router(auth_views.auth_router)
app.include_router(user_views.user_router)

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
