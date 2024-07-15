import logging
import os
import subprocess
import time
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI

from routes.main import router as main_router


# TODO: try a factory/builder to encapsulate dto instatiation logic
# TODO: investigate the infinite loop when a request to localhost is placed into a periodic task
# TODO: centralize dependencies creation to ensure consistency
# TODO: centralize temperature conversion from weather api
# TODO: check importing issue from main tests
# TODO: verify necessity of defining schema on postgres metadata in declarative_base
# TODO: make periodic() dependencies injectable to enable testing

load_dotenv()
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload_excludes=["./database/*"])
