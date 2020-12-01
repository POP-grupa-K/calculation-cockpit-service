import sys
import traceback

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from cockpit.exceptions.cockpit_exceptions import NoSuchTaskException
from cockpit.schema.cockpit_schema import CockpitSchema
from cockpit.service.cock_service import create_task, get_all_tasks_as_json_list, get_task_schema
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


@router.get("/", tags=["Backend Cockpit"])
async def list_tasks(db: Session = Depends(get_db)):
    tasks = get_all_tasks_as_json_list(db)
    if tasks is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(tasks))

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/add", tags=["Backend AppStore"])
async def add_task(cock: CockpitSchema, db: Session = Depends(get_db)) -> str:
    try:
        cock_id = create_task(cock, db)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=encode_to_json_message(cock_id))

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))


@router.get("/{id_task}", tags=["Backend Cockpit"])
async def get_task(id_task: int, db: Session = Depends(get_db)):
    try:
        task: CockpitSchema = get_task_schema(id_task, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(task))
    except NoSuchTaskException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message(f"No task with id = {id_task}"))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))

