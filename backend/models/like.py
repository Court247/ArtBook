from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from db.database import Base
from datetime import datetime

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='user_post_unique'),)
