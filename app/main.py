from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import engine, Base
from app.api.user import router as userRouter
from app.api.Admin import router as adminRouter
from app.api.Login import router as loginRouter

app = FastAPI(title="Registration")

app.include_router(loginRouter)
app.include_router(adminRouter)
app.include_router(userRouter)
