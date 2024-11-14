import fastapi
import fastapi.middleware
import fastapi.middleware.cors
import uvicorn

from src.api.hello import router as hello_world
from src.api.user.api import auth_router, users_router

app = fastapi.FastAPI()

app.include_router(hello_world)
app.include_router(auth_router)
app.include_router(users_router)

allows_origins = [
    "http://localhost:4200",
    "http://localhost:8080",
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
