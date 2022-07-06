import json
import time
from uuid import uuid4

from authlib.jose import JsonWebSignature
from authlib.jose.errors import DecodeError
from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, UUIDType
import datetime
from apps.postapp import Post
from core.config import SECRET_KEY
from db.base_class import Base


class User(Base):
    uid = Column(UUIDType, default=uuid4, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    email = Column(EmailType)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    post = relationship("Post", back_populates="owner")

    def get_reset_token(self, expires_sec=1800):
        jws = JsonWebSignature()
        protected = {'alg': 'HS256'}
        payload = json.dumps({'expires_sec': expires_sec,
                              'time_sending': time.time(),
                              'user_uid': str(self.uid)}).encode('utf-8')
        secret = SECRET_KEY
        return jws.serialize_compact(protected, payload, secret).decode('utf-8')

    @staticmethod
    def get_payload_from_reset_token(token):

        jws = JsonWebSignature()
        data = jws.deserialize_compact(token, SECRET_KEY)
        payload_json = json.loads(data['payload'])

        time_left = payload_json['time_sending'] + payload_json['expires_sec'] - time.time()
        print(time_left)

        if time_left < 0:
            return False
        else:
            return payload_json

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
