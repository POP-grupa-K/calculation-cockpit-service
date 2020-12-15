from datetime import datetime

from sqlalchemy.orm import Session

from cockpit.exceptions.cockpit_exceptions import NoSuchTaskException, TaskIsAlreadyRunningException, \
    TaskIsAlreadyStoppedException, TaskAppNotAvailable
from cockpit.model.cockpit_model import CockpitModel
from cockpit.model.user_app_model import UserAppModel
from cockpit.schema.cockpit_schema import CockpitSchema
from typing import List
import requests

from cockpit.schema.user_app_schema import UserAppSchema
from cockpit.utils.mapper.cockpit_mapper import cockpit_model_to_schema


def create_task(app: CockpitSchema, db: Session) -> int:
    new_task = CockpitModel.from_schema(app)
    if not check_if_app_is_available(app.id_app):
        raise TaskAppNotAvailable(f"App with id = {app.id_app} is not availble")
    new_task.date_update = datetime.now().isoformat()

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task.id_task


def get_all_tasks(db: Session) -> List[CockpitModel]:
    tasks_models = db.query(CockpitModel).filter(CockpitModel.status != "deleted")
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
        res = requests.get("http://appstore:8005/appstore/{}".format(task_model.id_app))
        if res.status_code == 200:
            app_details = res.json()
            app_name = app_details["nameApp"]
        else:
            app_name = str(task_model.id_app)

        task = {
            "appId": task_model.id_app,
            "appName": app_name,
            "tasks": [cockpit_model_to_schema(task_model).json()]
        }
        return task
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

    user_apps = []
    for id_app in set([task.id_app for task in user_tasks]):
        # FIXME url w envach trzeba trzymac
        res = requests.get("http://appstore:8005/appstore/{}".format(id_app))
        if res.status_code == 200:
            app_details = res.json()
            app_name = app_details["nameApp"]
        else:
            app_name = str(id_app)

        app = {
            "appName": app_name,
            "tasks": tasks_to_json_list(user_tasks.filter(CockpitModel.id_app == id_app))
        }
        user_apps.append(app)

    return user_apps


def set_task_status_to_running(id_task: int, db: Session):
    task: CockpitModel = get_task_model(id_task, db)
    if task:
        if not check_if_app_is_available(task.id_app):
            raise TaskAppNotAvailable(f"App with id = {task.id_app} is not availble")
        if task.status == "ongoing":
            raise TaskIsAlreadyRunningException(f"Task with id = {id_task} is already running")
        task.status = "ongoing"
        db.commit()
    else:
        raise NoSuchTaskException(f"No task with id = {id_task}")


def check_if_app_is_available(id_app: int):
    # FIXME url w envach trzeba trzymac
    res = requests.get("http://appstore:8005/appstore/{}".format(id_app))    
    if (res.status_code == 200):
        app_details = res.json()
        if (app_details['status'] == 'available'):
            return True
    return False


def delete_task(id_task: int, db: Session):
    task = get_task_model(id_task, db)
    if task is None:
        raise NoSuchTaskException(f"No task with id = {id_task}")

    db.delete(task)
    db.commit()


def set_task_status_to_stopped(id_task: int, db: Session):
    task: CockpitModel = get_task_model(id_task, db)
    if task:
        if task.status == "stopped":
            raise TaskIsAlreadyStoppedException(f"Task with id = {id_task} is already stopped")
        task.status = "stopped"
        db.commit()
    else:
        raise NoSuchTaskException(f"No task with id = {id_task}")


def add_app_to_cockpit(user_app: UserAppSchema, db: Session):
    new_app = UserAppModel.from_schema(user_app)
    if not check_if_app_is_available(user_app.id_app):
        raise TaskAppNotAvailable(f"App with id = {user_app.id_app} is not availble")

    new_task = CockpitModel(name="task", reserved_credits="0", id_app=user_app.id_app, status="created", priority="-1", id_user=user_app.id_user)
    new_task.date_update = datetime.now().isoformat()

    db.add(new_task)
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
