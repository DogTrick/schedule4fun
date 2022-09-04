# DB connection
from sqlalchemy import create_engine

db_name = "system.db"
db_connect_string = f"sqlite:///{db_name}"

engine = create_engine(db_connect_string)
from tables import Base
Base.metadata.create_all(engine)

# create session
from sqlalchemy.orm import sessionmaker, scoped_session
Session = sessionmaker(bind = engine, expire_on_commit = False)
Session = scoped_session(Session)

from contextlib import contextmanager
@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
