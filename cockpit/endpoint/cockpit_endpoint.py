from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from run import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", tags=["Backend AppStore"])
async def list_apps(db: Session = Depends(get_db)):

    return JSONResponse(status_code=status.HTTP_200_OK, content="69")
