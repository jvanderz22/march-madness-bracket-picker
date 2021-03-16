import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager

engine = create_engine(os.getenv("MARCH_MADNESS_BRACKET_PICKER_DB"))
Session = sessionmaker()
Session.configure(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
