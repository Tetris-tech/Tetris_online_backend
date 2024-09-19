from fastapi import APIRouter

router = APIRouter(prefix="/hello")


@router.get("/world")
async def hello_world() -> dict[str, str]:
    """Test endpoint to connect frontend with backend."""
    return {"message": "Hello, world!"}