from fastapi import FastAPI
import uvicorn

from .configs import app_settings
from .utils import lifespan

from .apps import auth_router, employees_router


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router, prefix="/login", tags=["Auth"])
app.include_router(employees_router, prefix="/employees", tags=["Employees"])


if __name__ == "__main__":
    uvicorn.run("main:app", port=app_settings.app.port, reload=True, host=app_settings.app.host)
