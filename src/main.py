import fastapi
import fastapi.middleware
import fastapi.middleware.cors
import uvicorn

from src.api.hello import router as hello_world
from src.api.user import router as user_router

app = fastapi.FastAPI()

app.include_router(hello_world)
app.include_router(user_router)

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
