from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_url = 'postgresql://myuser:mypassword@localhost/UserManagement'
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

test_db_url = 'sqlite:///test.db'
test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def get_db(test_db: bool = False):
    if test_db:
        db = TestSessionLocal()
    else:
        db = SessionLocal()
    try:
        yield db
    finally:
        db.close()