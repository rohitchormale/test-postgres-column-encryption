import json
from sqlalchemy_utils import JSONType, StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from sqlalchemy import types as sqtypes
from .extensions import db


# head -c32 /dev/urandom | python -m base64
DB_ENCRYPTION_KEY = "<I-M-NOT-UR-REAL-KEY-CHANGE-ME>"



################
# Helper models
################


class BaseModel(db.Model):
    """
    Abstract model
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            try:
                getattr(self, key)
                setattr(self, key, value)
            except AttributeError:
                pass

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# TODO - Add your models here  e.g.
# class User(BaseModel):
#     pass


# When writing this PoC, `sqlalchemy_utils.JSONType` doesn't work properly with `sqlalchemy.StringEncryptedType`
# On reading, it returns string instead of dict/list. So we will use custom JsonType
# see https://github.com/kvesteri/sqlalchemy-utils/issues/532

class JsonType(sqtypes.TypeDecorator):
    impl = sqtypes.TEXT

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)

    def copy(self, **kwargs):
        return JsonType(self.impl.length)


class UserModel(BaseModel):
    __tablename__ = 'users'
    name = db.Column(db.String())
    password = db.Column(StringEncryptedType(db.String, DB_ENCRYPTION_KEY, AesEngine, "pkcs5"))
    ccdetails = db.Column(StringEncryptedType(JsonType, DB_ENCRYPTION_KEY, AesEngine, "pkcs5"))
    ccdetails2 = db.Column(JSONType())

def __repr__(self):
    return f"<User {self.name}>"