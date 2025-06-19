# main.py

from fastapi import FastAPI
from routers import gui_user
from routers.policy import router as admin_policy_router
from models import Base
from database import engine

Base.metadata.create_all(bind=engine) #해당 코드를 통해 테이블 생성 가능. 한번만 생성.(중복생성 안함)

app = FastAPI()
app.include_router(gui_user.router)
app.include_router(admin_policy_router)

@app.get("/")
def root():
    return {"message": "DRM API is running!"}

# 실행: uvicorn main:app --reload