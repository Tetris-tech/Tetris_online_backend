import fastapi
import fastapi.middleware
import fastapi.middleware.cors
import uvicorn

from src.user.api import views as user_views
from src.auth.api import views as auth_views
from src.user import admin
import config
from sqladmin import Admin

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

if __name__=="__main__":
    uvicorn.run(app)
