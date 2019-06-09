from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Project(Base):
    __tablename__ = 'issue_token_project'

    id = Column(Integer, primary_key=True)
    circulator = Column(String, unique=True)
    issuer = Column(String, unique=True, nullable=True)
    issuer_sk = Column(String, unique=True, nullable=True)
    status = Column(Integer, default=0)  # 0 created, 1 finished
