from fastapi import FastAPI
from .Routes.products import products_router
from .Routes.users import users_router
from .Models import Base
from .Database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(products_router)
app.include_router(users_router)
