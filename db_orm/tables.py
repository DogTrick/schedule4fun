from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Account(Base):
    __tablename__ = "account"
    
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    
    schedule = relationship("Schedule", backref = "account", cascade = "all")
    
class Schedule(Base):
    __tablename__ = "schedule"    
    
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("account.id"))
    user_name = Column(String(50), nullable=False)
    title = Column(String(50))
    content = Column(String(300))
    datetime = Column(DateTime, default = datetime.now())
    