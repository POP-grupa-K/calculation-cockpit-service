from sqlalchemy import String, Column, DateTime, Integer

from cockpit.schema import cockpit_schema
from run import Base


class CockpitModel(Base):
    __tablename__ = 'cockpit'

    # don't blame me, blame the devops for weird field naming
    id_task = Column('idtask', Integer, primary_key=True)
    name = Column('name', String)
    version = Column('version', Integer)
    date_start = Column('datestart', DateTime)
    date_end = Column('dateend', DateTime)
    consumed_credits = Column('consumedcredits', String)
    reserved_credits = Column('reservedcredits', String)
    status = Column('status', String)
    priority = Column('priority', Integer)
    private = Column('private', String)
    cluster_allocation = Column('clusterallocation', String)
    id_app = Column('idapp', Integer)
    id_user = Column('iduser', Integer)

    def __init__(self, name, reservedcredits, id_app, status, id_user):
        self.name = name
        self.reserved_credits = reservedcredits
        self.id_app = id_app
        self.status = status
        self.id_user = id_user

    @classmethod
    def from_schema(cls, cockpit_schema: cockpit_schema.CockpitSchema):
        return cls(cockpit_schema.name, cockpit_schema.reservedcredits, cockpit_schema.idapp, cockpit_schema.status, cockpit_schema.iduser)
