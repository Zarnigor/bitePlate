import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.production")
django.setup()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from django.core.asgi import get_asgi_application
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from apps.menu.api         import router as menu_router
from apps.orders.api       import router as orders_router
from apps.kitchen.api      import router as kitchen_router
from apps.billing.api      import router as billing_router
from apps.tables.api       import router as tables_router
from apps.reservations.api import router as reservations_router

api = FastAPI(title="BitePlate API", version="1.0.0",
              docs_url="/api/docs", redoc_url="/api/redoc")

api.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"])

for router in [tables_router, reservations_router, orders_router,
               kitchen_router, menu_router, billing_router]:
    api.include_router(router, prefix="/api")

django_app = get_asgi_application()

application = Starlette(routes=[
    Mount("/api",  app=api),
    Mount("/",     app=django_app),
])
