import fastapi.middleware
import fastapi.middleware.cors
import uvicorn

from src.middleware import BlacklistTokenCheckMiddleware
from src.api.hello import router as hello_world
from src.api.user.api import auth_router, users_router

app = fastapi.FastAPI()

app.include_router(hello_world)
app.include_router(auth_router)
app.include_router(users_router)

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

# Define paths where token should be checked (e.g., /protected-endpoint)
#blacklist_paths = ["/protected-endpoint", "/some/other/path"]
blacklist_paths = []

# Add middleware
app.add_middleware(BlacklistTokenCheckMiddleware, paths=blacklist_paths)

if __name__=="__main__":
    uvicorn.run(app)
