import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Clase para definir el esquema de la tabla en la base de datos
Base = declarative_base()


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    audience = Column(String, nullable=False)
    type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    unread = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
