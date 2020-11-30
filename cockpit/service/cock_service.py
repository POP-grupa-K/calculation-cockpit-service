from datetime import datetime

from sqlalchemy.orm import Session


from cockpit.model.cockpit_model import CockputModel
from cockpit.schema.cockpit_schema import CockpitSchema


def create_task(app: CockpitSchema, db: Session) -> int:
    new_task = CockputModel.from_schema(app)

    new_task.date_update = datetime.now().isoformat()

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task.id_app