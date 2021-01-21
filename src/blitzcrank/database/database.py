
import logging
import typing

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

logger: logging.Logger = logging.getLogger(__name__)


class Database:
    def __init__(
        self,
        session: typing.Union[Session, None] = None,
        engine: typing.Union[Engine, None] = None,
        base: typing.Union[typing.Any, None] = None,
    ):
        """Initizalize service.  Vars are for testing.

        Args:
            session (Session, None): Session object. Defaults to None.
            engine (Engine, None): Engine object. Defaults to None.
            base (Base, None): Base object. Defaults to None.
        """
        self.session: typing.Union[Session, None] = session
        self.engine: typing.Union[Engine, None] = engine
        self.base: typing.Union[typing.Any, None] = base

    def get_session(self) -> typing.Union[Session, None]:
        """Creates new session if none exist.

        Returns:
            typing.Union[Session, None]: returns Session
        """
        if self.session is None:
            Session = sessionmaker()
            Session.configure(bind=self.get_engine())
            self.session = Session()
        return self.session

    def get_engine(self) -> typing.Union[Engine, None]:
        """Creates a new engine if none exist.

        Returns:
            typing.Union[Engine, None]: returns Engine
        """
        if self.engine is None:
            self.engine = create_engine(f"sqlite:///test.db") # TODO Extract
        return self.engine

    def get_base(self) -> typing.Union[typing.Any, None]:
        """Creates a new base if none exist.

        Returns:
            typing.Union[typing.Any, None]: returns Base
        """
        if self.base is None:
            self.base = declarative_base()
        return self.base
