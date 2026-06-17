from fastapi import FastAPI
from routers import urls, auth

app = FastAPI()

app.include_router(urls.router)
app.include_router(auth.router)