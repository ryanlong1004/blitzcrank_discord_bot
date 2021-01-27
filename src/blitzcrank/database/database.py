import logging
import typing

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger: logging.Logger = logging.getLogger(__name__)

BASE = declarative_base()
ENGINE: Engine = create_engine(f"sqlite:///test.db")  # TODO Extract
SESSION: typing.Any = sessionmaker()
SESSION.configure(bind=ENGINE)
