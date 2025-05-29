from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL =  "postgresql+psycopg2://postgres:1234@localhost/drm_db" # 실제 접속 정보에 맞게 수정할것


engine = create_engine(DATABASE_URL)   # 엔진 생성 
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)   # 세션 팩토리 생성

# 의존성 주입용 DB 세션 생성기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
