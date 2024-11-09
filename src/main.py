import fastapi
import uvicorn

from src.api.hello import router as hello_world
from src.api.user import router as user_router

app = fastapi.FastAPI()

app.include_router(hello_world)
app.include_router(user_router)


if __name__=="__main__":
    uvicorn.run(app)
