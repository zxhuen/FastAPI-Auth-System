from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import engine, Base
from app.api.user import router as userRouter

import app.models

app = FastAPI(title="Registration")

app.include_router(userRouter)