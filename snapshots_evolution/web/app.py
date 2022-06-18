from fastapi import FastAPI
from web.views import router

app = FastAPI()
app.include_router(router)
