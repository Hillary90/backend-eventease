from fastapi import APIRouter

router = APIRouter()

@router.get("/test-auth")
def test_auth():
    return {"message": "Auth route works"}
