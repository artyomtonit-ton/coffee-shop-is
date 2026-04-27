from fastapi import FastAPI

from app.admin.router import router as admin_router
from app.auth.router import router as auth_router
from app.config import settings
from app.loyalty.router import router as loyalty_router
from app.menu.router import router as menu_router
from app.orders.router import router as orders_router
from app.users.router import router as users_router


app = FastAPI(
    title=settings.app_name,
    description="Diploma project: information system for a coffee shop",
    version=settings.app_version,
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(menu_router)
app.include_router(orders_router)
app.include_router(loyalty_router)
app.include_router(admin_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
