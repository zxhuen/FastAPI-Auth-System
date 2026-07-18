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

from app.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI(title="Registration")

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(SlowAPIMiddleware)

app.include_router(registerRouter)
app.include_router(loginRouter)
app.include_router(adminRouter)
app.include_router(userRouter)
app.include_router(refreshRouter)
app.include_router(authRouter)
app.include_router(forgetPasswordRouter)


