from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import engine, Base
from app.api.user import router as userRouter
from app.api.Admin import router as adminRouter
from app.api.Login import router as loginRouter
from app.api.refresh_token import router as refreshRouter
from app.api.auth import router as authRouter
from app.api.forget_password import router as forgetPasswordRouter
from app.api.Register import router as registerRouter

app = FastAPI(title="Registration")
app.include_router(registerRouter)
app.include_router(loginRouter)
app.include_router(adminRouter)
app.include_router(userRouter)
app.include_router(refreshRouter)
app.include_router(authRouter)
app.include_router(forgetPasswordRouter)


