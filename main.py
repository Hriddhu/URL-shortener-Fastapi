from fastapi import FastAPI
from routers import urls

app = FastAPI()

app.include_router(urls.router)