import sqlalchemy
from sqlalchemy import Column, Integer, Text, String, Enum, DateTime, ForeignKey, relationship
from sqlalchemy.dialects import ARRAY
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

_session = None
def init(backend="sqlite:///:memory:", verbose=False):
    global _session
    engine = sqlalchemy.create_engine(backend, echo=verbose)
    Base.metadata.create_all(engine) 
    Session = sessionmaker(bind=engine)
    _session = Session()

class UserNodeChild(Base):
    __tablename__ = "usernodechild"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('usernode.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    title = String(256)

class UserNode(Base):
    __tablename__ = "usernode"
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    parent = Column(Integer, ForeignKey('id'))
    owner = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime)
    base_node = Column(Integer, ForeignKey("id"))
    children = relationship("UserNodeChild", backref='usernode')

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    type = Column(Enum(['admin', 'teacher', 'student']))
    user_nodes = relationship("UserNode")
    completed_content = relationship("ContentNode")
    #owned_material = ...

class ContentNode(Base):
    __tablename__ = "contentnode"
    id = Column(Integer, primary_key=True)
    title = Column(String(512))
    description = Column(Text)
    creator = Column(ForeignKey('user.id'))
    knowledge_graph = None
    base_node = Column(ForeignKey('id'))
    grade_level = Column(Integer)
    recommended_time = Column(Integer)
    #materials = ...
    standards = Column(ARRAY(String))

_class_lookup = {
    "usernode" : UserNode,
    "user" : User,
    "contentnode" : ContentNode,
}

# TODO: write save/update/get/exists for base_sql

