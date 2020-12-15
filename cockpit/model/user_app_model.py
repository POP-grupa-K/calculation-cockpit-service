from sqlalchemy import String, Column, DateTime, Integer

from cockpit.schema import user_app_schema
from run import Base


class UserAppModel(Base):
    __tablename__ = 'user_app'

    # don't blame me, blame the devops for weird field naming
    id_user_app = Column('iduserapp', Integer, primary_key=True)
    id_app = Column('idapp', String)
    id_user = Column('iduser', Integer)

    def __init__(self, id_app, id_user):
        self.id_app = id_app
        self.id_user = id_user

    @classmethod
    def from_schema(cls, user_app_schema: user_app_schema.UserAppSchema):
        return cls(user_app_schema.id_app, user_app_schema.id_user)
