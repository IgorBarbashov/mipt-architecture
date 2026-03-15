from db import Base
from sqlalchemy import Column, DateTime, Integer, String, func


class Errors(Base):
    __tablename__ = "errors"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    code = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    details = Column(String, nullable=False)
