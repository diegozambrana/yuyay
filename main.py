from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes import github, pystats, yahoo_finance, tracker


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(yahoo_finance.router)
app.include_router(github.router)
app.include_router(pystats.router)
app.include_router(tracker.router)