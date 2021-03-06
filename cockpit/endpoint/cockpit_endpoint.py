import sys
import traceback

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status

from cockpit.exceptions.cockpit_exceptions import NoSuchTaskException, TaskIsAlreadyRunningException, \
    TaskIsAlreadyStoppedException, TaskAppNotAvailable
from cockpit.schema.cockpit_schema import CockpitSchema
from cockpit.schema.user_app_schema import UserAppSchema
from cockpit.service.cockpit_service import create_task, get_all_tasks_as_json_list, get_task_schema, \
    get_task_models_by_status_and_app, tasks_to_json_list, update_task, set_task_status_to_running, \
    set_task_status_to_stopped, get_all_user_tasks, delete_task, add_app_to_cockpit
from cockpit.utils.message_encoder.json_message_encoder import encode_to_json_message
from run import SessionLocal
from fastapi.responses import JSONResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", tags=["Backend Cockpit - ICockpitCrud"])
async def list_tasks(states: str = "created", db: Session = Depends(get_db)):
    tasks = get_all_tasks_as_json_list(states, db)
    if tasks is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(tasks))

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/", tags=["Backend Cockpit - ICockpitCrud"])
async def add_task(cock: CockpitSchema, db: Session = Depends(get_db)):
    try:
        cock_id = create_task(cock, db)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=encode_to_json_message(cock_id))

    except TaskAppNotAvailable as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=encode_to_json_message(f"App from task is not available"))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))


@router.put("/{id_task}", tags=["Backend Cockpit - ICockpitCrud"])
async def edit_task(id_task: int, cock: CockpitSchema, db: Session = Depends(get_db)):
    try:
        task: CockpitSchema = update_task(id_task, cock, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(task))
    except NoSuchTaskException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message(f"No task with id = {id_task}"))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))


@router.get("/{id_task}", tags=["Backend Cockpit - ICockpitCrud"])
async def get_task(id_task: int, db: Session = Depends(get_db)):
    try:
        task: CockpitSchema = get_task_schema(id_task, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(task))
    except NoSuchTaskException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message(f"No task with id = {id_task}"))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))


@router.get("/{id_app}/{task_status}", tags=["Backend Cockpit - ICockpitCrud"])
async def get_tasks_for_app(id_app: int, task_status: str, db: Session = Depends(get_db)):
    task_models = get_task_models_by_status_and_app(id_app, task_status, db)
    tasks = tasks_to_json_list(task_models)
    if tasks is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(tasks))

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/user/tasks/{id_user}", tags=["Backend Cockpit - ICockpitCrud"])
async def get_user_tasks(id_user: int, db: Session = Depends(get_db)):
    try:
        user_tasks = get_all_user_tasks(id_user, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user_tasks))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))


@router.post("/{id_task}/run", tags=["Backend Cockpit - ICockpitCrud"])
async def run_task(id_task: int, db: Session = Depends(get_db)):
    try:
        set_task_status_to_running(id_task, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message(f"Task with id = {id_task} is running"))
    except NoSuchTaskException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message(f"No task with id = {id_task}"))
    except TaskIsAlreadyRunningException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=encode_to_json_message(f"Task with id = {id_task} is already running"))
    except TaskAppNotAvailable as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=encode_to_json_message(f"App from task is not availble"))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))


@router.post("/{id_task}/stop", tags=["Backend Cockpit - ICockpitCrud"])
async def stop_task(id_task: int, db: Session = Depends(get_db)):
    try:
        set_task_status_to_stopped(id_task, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message(f"Task with id = {id_task} is stopped"))
    except NoSuchTaskException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message(f"No task with id = {id_task}"))
    except TaskIsAlreadyStoppedException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=encode_to_json_message(f"Task with id = {id_task} is already stopped"))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))


@router.delete("/{id_task}", tags=["Backend Cockpit - ICockpitCrud"])
async def delete_task_by_id(id_task: int, db: Session = Depends(get_db)):
    try:
        delete_task(id_task, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message("OK"))
    except NoSuchTaskException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message(f"No task with id = {id_task}"))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/apps", tags=["Backend Cockpit - ICockpitCrud"])
async def add_app(user_app_schema: UserAppSchema, db: Session = Depends(get_db)):
    try:
        add_app_to_cockpit(user_app_schema, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message("OK"))
    except TaskAppNotAvailable as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=encode_to_json_message(f"App with given id is not available"))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
