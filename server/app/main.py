from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.email import router as email_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_router)

@app.on_event("startup")
async def on_startup():
    # await create_db_and_tables()
    print('Started')