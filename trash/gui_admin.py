from fastapi import APIRouter, HTTPException 
from pydantic import BaseModel 
from typing import Optional

router = APIRouter()

request_store = {}

class DecisionPayload(BaseModel):
    decision: str   # 승인 혹은 거절
    deny_reason: Optional[str] = None  # 거절일 때만 사용됨


@router.post("/request/{request_id}/decision")
def decide_request(request_id: str, payload: DecisionPayload):
    if request_id not in request_store:
        raise HTTPException(status_code=404, detail="요청이 존재하지 않습니다.")

    if payload.decision not in ("approve", "deny"):
        raise HTTPException(status_code=400, detail="결정은 approve 또는 deny 여야 합니다.")

    request = request_store[request_id]
    request["state"] = payload.decision

    if payload.decision == "deny":
        request["deny_reason"] = payload.deny_reason or "사유 없음"

    return { "message": f"요청이 {payload.decision} 상태로 처리되었습니다." }

@router.get("/requests/recent")
def get_recent_requests():
    return sorted(request_store.values(), key=lambda x: x["created_at"], reverse=True)[:10]    

@router.get("/requests/count")
def get_request_count():
    return len(request_store)
