import fastapi
import uvicorn

from src.api.hello import router as hello_world

app = fastapi.FastAPI()

app.include_router(hello_world)


if __name__=="__main__":
    uvicorn.run(app)
