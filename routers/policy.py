from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
import random 
import pytz
import string

router = APIRouter()

# 메모리 저장소
general_policies = {}
exception_policies = {}
general_id_counter = 1
exception_id_counter = 1

# ─── 유틸: 10자리 랜덤 ID 생성 ───
def generate_id(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ─── 모델 ───
class GeneralPolicy(BaseModel):
    target_ou: str
    required_min_rank: int

class GeneralPolicyOut(GeneralPolicy):
    id: str
    target_ou: str
    required_min_rank: int
    created_at: str

class ExceptionPolicy(BaseModel):
    file_hash: str
    user_guid: str
    valid_until: str  # 'YYYY-MM-DD HH:MM:SS' 형식 문자열 (KST)
    
class ExceptionPolicyOut(BaseModel):
    id: str
    file_hash: str
    user_guid: str
    action: str = "allow"
    valid_until: str
    created_at: str

# ─── 일반 정책 등록 ───
@router.post("/admin/policy", response_model=GeneralPolicyOut)
def create_general_policy(policy: GeneralPolicy):
    id = generate_id()
    now_kst = datetime.now(pytz.timezone("Asia/Seoul")).strftime('%Y-%m-%d %H:%M:%S')
    data = {
        "id": id,
        "target_ou": policy.target_ou,
        "required_min_rank": policy.required_min_rank,
        "created_at": now_kst
    }
    general_policies[id] = data
    return data

# ─── 예외 정책 등록 ───
@router.post("/admin/policy/exception", response_model=ExceptionPolicyOut)
def create_exception_policy(policy: ExceptionPolicy):
    id = generate_id()
    now_kst = datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    policy_data = {
        "id": id,
        "file_hash": policy.file_hash,
        "user_guid": policy.user_guid,
        "action": "allow",
        "valid_until": policy.valid_until,
        "created_at": now_kst
    }
    exception_policies[id] = policy_data
    return policy_data


# ─── 일반 정책 전체 조회 ───
@router.get("/admin/policy", response_model=list[GeneralPolicyOut])
def get_all_general_policies():
    return list(general_policies.values())

# ─── 예외 정책 전체 조회 ───
@router.get("/admin/policy/exception", response_model=list[ExceptionPolicyOut])
def get_all_exception_policies():
    return list(exception_policies.values())

# ─── 일반 정책 수정 ───
@router.put("/admin/policy/{policy_id}", response_model=GeneralPolicyOut)
def update_general_policy(policy_id: str, updated: GeneralPolicy):
    if policy_id not in general_policies:
        raise HTTPException(status_code=404, detail="정책 없음")
    policy_data = updated.dict()
    policy_data["id"] = policy_id
    policy_data["created_at"] = general_policies[policy_id]["created_at"]
    general_policies[policy_id] = policy_data
    return policy_data

# ─── 예외 정책 수정 ───
@router.put("/admin/policy/exception/{exception_id}", response_model=ExceptionPolicyOut)
def update_exception_policy(exception_id: str, updated: ExceptionPolicy):
    if exception_id not in exception_policies:
        raise HTTPException(status_code=404, detail="예외 정책 없음")
    policy_data = updated.dict()
    policy_data["id"] = exception_id
    policy_data["action"] = "allow"  # 수정 시에도 고정
    policy_data["created_at"] = exception_policies[exception_id]["created_at"]
    exception_policies[exception_id] = policy_data
    return policy_data