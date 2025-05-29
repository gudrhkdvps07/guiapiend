#test.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/ping", summary= "헬스체크", description= "이 api는 서버가 살아있는지 체크하는 용도.")
def ping():
	return {"message": "pong"}