from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    caption = Column(Text)
    image_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_flagged = Column(Boolean, default=False)

    user = relationship("User")
