from uuid import uuid4

from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, UUIDType
import datetime
from apps.postapp import Post
from db.base_class import Base


class User(Base):
    uid = Column(UUIDType, default=uuid4, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    email = Column(EmailType)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    post = relationship("Post", back_populates="owner")

    def __repr__(self):
        info = f'<User [username: {self.username}, email: {self.email}]>'
        return info


class Token(Base):
    uid = Column(UUIDType, default=uuid4, primary_key=True)
    token = Column(UUIDType, unique=True, nullable=False, index=True, default=uuid4)
    expires = Column(DateTime())
    user_uid = Column(UUIDType, ForeignKey('user.uid'))

    def __repr__(self):
        return f'<User [user_uid: {self.user_uid}, expires: {self.expires}, token: {self.token}]>'

