from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Flow(Base):
    __tablename__ = "flows"
    id = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    payload = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class FlowRun(Base):
    __tablename__ = "flow_runs"
    id = Column(String(255), primary_key=True, index=True)
    flow_id = Column(String(255), nullable=False, index=True)
    status = Column(String(50), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
