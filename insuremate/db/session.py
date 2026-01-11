from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from insuremate.core.config import DATABASE_URL, get_sqlalchemy_connect_args

connect_args = get_sqlalchemy_connect_args()

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args if connect_args is not None else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
