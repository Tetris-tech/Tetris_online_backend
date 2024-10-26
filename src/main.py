import fastapi
import uvicorn

from src.api.hello import router as hello_world
from src.api.user_routes import router as user_router  # Import the user router

app = fastapi.FastAPI()

app.include_router(hello_world) #TODO: delete?!
app.include_router(user_router)  # Register the user-related routes

if __name__ == "__main__":
    uvicorn.run(app)
