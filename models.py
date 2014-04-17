from sqlalchemy import (
    Column,
    Integer,
    Text,
    Numeric
    )

from sqlalchemy.ext.declarative import declarative_base
from pyramid.renderers import JSON
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    data = Column(Numeric)
    url = Column(Text)

    def __init__(self, name, data, url):
        self.name = name
        self.data = data
        self.url = url
