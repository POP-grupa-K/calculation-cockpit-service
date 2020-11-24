import os
import uvicorn as uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.middleware.cors import CORSMiddleware

from cockpit.endpoint import cockpit_endpoint

app = FastAPI(title="System obliczeń wysokoskalowych")

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

origins = [
    "*"
]

if __name__ == "__main__":
    app.include_router(cockpit_endpoint.router, prefix="/cockpit")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    uvicorn.run(app, host="0.0.0.0", port=8006)

