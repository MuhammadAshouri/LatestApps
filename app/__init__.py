import logging

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi_responses import custom_openapi

from config import DOCS

__version__ = "0.1"


app = FastAPI(
    title="Latest Apps",
    description="Simple Project To Download Latest Version Of VPN Clients.",
    version=__version__,
    docs_url='/docs' if DOCS else None,
    redoc_url='/redoc' if DOCS else None
)
app.openapi = custom_openapi(app)
scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2}, timezone='UTC')
logger = logging.getLogger('uvicorn.error')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app import  views, jobs  # noqa

def use_route_names_as_operation_ids(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name

use_route_names_as_operation_ids(app)


@app.on_event("startup")
def on_startup():
    scheduler.start()


@app.on_event("shutdown")
def on_shutdown():
    scheduler.shutdown()


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = {}
    for error in exc.errors():
        details[error["loc"][-1]] = error.get("msg")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": details}),
    )