from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class TaskRun(Base):
    __tablename__ = "task_runs"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    run_id = Column(String(255), nullable=False, index=True)
    task_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    output = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.now)
    finished_at = Column(DateTime, nullable=True)

class TaskRegistry(Base):
    __tablename__ = "tasks"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_name = Column(String(255), nullable=False, unique=True)
    impl_path = Column(String(512), nullable=False)  # module:Class
