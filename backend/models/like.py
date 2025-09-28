from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from db.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Like(Base):
    __tablename__ = "likes"

    id = Column(String(36), primary_key=True, index=True)  # UUID for likes
    user_id = Column(String(128), ForeignKey("users.firebase_uid", ondelete="CASCADE"))
    post_id = Column(String(36), ForeignKey("posts.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "post_id", name="unique_user_post"),)
    
    # Relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes") 