from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    page_id = Column(String, unique=True, index=True)  # ID صفحة الفيسبوك
    api_key = Column(String)  # مفتاح API لاستخدام الذكاء الاصطناعي

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sender_id = Column(String)
    message_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
