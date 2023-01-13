import os
import pytest
from typing import Generator

from app.db.base_class import Base
from app.tests import SessionLocal
from app.tests.utils.yaml_to_db import YamlToDB
from sqlalchemy.orm import scoped_session


@pytest.fixture()
def db() -> Generator:
    # import pdb
    # pdb.set_trace()
    local_session = SessionLocal()
    Base.metadata.create_all(bind=local_session.bind)
    yield local_session
    # scoped_session(local_session).remove()
    local_session.close_all()
    Base.metadata.drop_all(bind=local_session.bind, checkfirst=False)


@pytest.fixture()
def models(db, request):
    """Fill database from yaml models description"""

    filepath = os.path.join(request.fspath.dirname, 'models.yml')

    if os.path.isfile(filepath):
        models = YamlToDB(filepath, 'app.models', db)
        models.save_all()
        yield models
    else:
        yield []
