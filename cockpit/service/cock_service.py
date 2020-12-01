from datetime import datetime

from sqlalchemy.orm import Session


from cockpit.model.cockpit_model import CockpitModel
from cockpit.schema.cockpit_schema import CockpitSchema
from typing import List

from cockpit.utils.mapper.cockpit_mapper import cockpit_model_to_schema


def create_task(app: CockpitSchema, db: Session) -> int:
    new_task = CockpitModel.from_schema(app)

    new_task.date_update = datetime.now().isoformat()

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task.id_app


def get_all_tasks(db: Session) -> List[CockpitModel]:
    tasks_models = db.query(CockpitModel).all()
    return tasks_models


def get_all_tasks_as_json_list(db: Session):
    tasks_models = get_all_tasks(db)

    tasks = []
    for task in tasks_models:
        tasks.append(cockpit_model_to_schema(task).json())
    return tasks