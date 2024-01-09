from decouple import config
from dotenv import load_dotenv

load_dotenv()

UVICORN_HOST = config("UVICORN_HOST", default="0.0.0.0")
UVICORN_PORT = config("UVICORN_PORT", cast=int, default=8000)
UVICORN_UDS = config("UVICORN_UDS", default=None)
UVICORN_SSL_CERTFILE = config("UVICORN_SSL_CERTFILE", default=None)
UVICORN_SSL_KEYFILE = config("UVICORN_SSL_KEYFILE", default=None)


DEBUG = config("DEBUG", default=False, cast=bool)
DOCS = config("DOCS", default=False, cast=bool)

CUSTOM_TEMPLATES_DIRECTORY = config("CUSTOM_TEMPLATES_DIRECTORY", default=None)
HOME_PAGE_TEMPLATE = config("HOME_PAGE_TEMPLATE", default="home/index.html")

V2RAYNG=config("V2RAYNG", default="latest")
V2RAYN=config("V2RAYN", default="latest")
CLASH_META=config("CLASH_META", default="latest")
CLASH_VERGE=config("CLASH_VERGE", default="latest")
NEKOBOX_64=config("NEKOBOX_64", default="latest")
NEKOBOX_32=config("NEKOBOX_32", default="latest")
NEKORAY=config("NEKORAY", default="latest")
