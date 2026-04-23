from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/healthcheck")
def healthcheck():
    return {
        "status": "ok",
        "service": "knowledgepilot-ai",
        "version": "1.0.0"
    }