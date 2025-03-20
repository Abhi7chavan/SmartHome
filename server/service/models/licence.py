from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from typing import List
import random
import uuid

LicenseBase = declarative_base()

class LicenseDB(LicenseBase):
    __tablename__ = "licence"
    __table_args__ = {'schema': 'meta'} 

    id = Column(UUID(as_uuid=True), default=uuid.uuid1, primary_key=True, unique=True, index=True, nullable=False)
    name = Column(String, index=True)
    username = Column(String,unique =True)
    email = Column(String,unique=True)
    lastname = Column(String, index=True)
    location = Column(String, index=True)
    information = Column(ARRAY(String))
    householdItems = Column(ARRAY(String))
    submeters = Column(Integer)
class LicenseData(BaseModel):
    name: str
    username:str
    email:str
    lastname: str
    location: str
    information: List[str] = []  # Use List with the actual type
    householdItems: List[str] = []  # Use List with the actual type
    submeters: int

