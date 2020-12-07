from datetime import datetime

from sqlalchemy.orm import Session

from cockpit.exceptions.cockpit_exceptions import NoSuchTaskException
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
    return new_task.id_task


def get_all_tasks(db: Session) -> List[CockpitModel]:
    tasks_models = db.query(CockpitModel).all()
    return tasks_models


def get_all_tasks_as_json_list(db: Session):
    tasks_models = get_all_tasks(db)

    tasks = []
    for task in tasks_models:
        tasks.append(cockpit_model_to_schema(task).json())
    return tasks


def get_task_model(id_task: int, db: Session):
    task = db.query(CockpitModel).filter(CockpitModel.id_task == id_task)
    if task.first():
        return task.first()
    return None


def update_task(id_task: int, updated_task: CockpitSchema, db: Session):
    task_model: CockpitModel = get_task_model(id_task, db)
    if task_model is None:
        raise NoSuchTaskException(f"No task with id = {id_task}")
    task_model.name = updated_task.name
    task_model.version = updated_task.version
    task_model.status = updated_task.status
    db.commit()
    return cockpit_model_to_schema(task_model)


def get_task_schema(id_task: int, db: Session):
    task_model = get_task_model(id_task, db)
    if task_model:
        return cockpit_model_to_schema(task_model)
    raise NoSuchTaskException(f"No task with id = {id_task}")


def get_task_models_by_status_and_app(id_app: int, status: str, db: Session):
    tasks = db.query(CockpitModel).filter(CockpitModel.id_app == id_app).filter(CockpitModel.status == status)

    return tasks


def tasks_to_json_list(tasks_models):
    tasks = []
    for task in tasks_models:
        tasks.append(cockpit_model_to_schema(task).json())
    return tasks


def get_all_user_tasks(id_user, db: Session):
    user_tasks = db.query(CockpitModel).filter(CockpitModel.id_user == id_user)

    user_package = {}
    for id_app in set([task.id_app for task in user_tasks]):
        # TODO Getting App name from AppStore
        # r = requests.request('GET', 'https://localhost:8005/appstore/' + str(id_app))
        user_package["TODO-AppName" + str(id_app)] = tasks_to_json_list(user_tasks.filter(CockpitModel.id_app == id_app))

    return user_package
