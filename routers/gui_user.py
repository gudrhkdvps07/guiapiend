# gui_user.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

from models import FileRequest
from database import get_db

router = APIRouter()

class RequestPayload(BaseModel):
    user_hash: str
    user_name: str
    file: str
    deny_reason: Optional[str] = None
    request_body: Optional[str] = None

@router.post("/request")
def send_request(payload: RequestPayload, db: Session = Depends(get_db)):
    request_id = str(uuid.uuid4())[:8]

    new_req = FileRequest(
    id=request_id,
    user_hash=payload.user_hash,
    user_name=payload.user_name,
    file=payload.file,
    request_body=payload.request_body,
    deny_reason=payload.deny_reason,
)
    db.add(new_req)
    db.commit()
    return {
        "request_id": request_id,
        "message": "요청이 정상적으로 접수되었습니다."
    }


@router.get("/request/{request_id}") #확인용 코드
def get_request(request_id: str, db: Session = Depends(get_db)):
    req = db.query(FileRequest).filter(FileRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="요청이 존재하지 않습니다.")
    return req