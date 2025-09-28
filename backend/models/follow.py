from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Follow(Base):
    __tablename__ = "follows"

    id = Column(String(36), primary_key=True, index=True)  # UUID for follows
    follower_id = Column(String(128), ForeignKey("users.firebase_uid", ondelete="CASCADE"), nullable=False)
    following_id = Column(String(128), ForeignKey("users.firebase_uid", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships (self-referential many-to-many)
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")

    __table_args__ = (
        UniqueConstraint("follower_id", "following_id", name="unique_follow"),
    )
