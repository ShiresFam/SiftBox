from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.email import router as auth_router
from app.api.email import mail_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


origins = [
    "https://foodfresh-web-dwxlwryksa-uk.a.run.app",
    "https://foodfresh-web-dwxlwryksa-uk.a.run.app/*",
    "https://foodfreshco.com",
    "https://foodfreshco.com/*",
    "http://localhost",
    "http://localhost/*",
    "http://localhost:3000",
    "http://localhost:3000/*",
    "http://192.168.1.175",
    "http://192.168.1.175/*",
    "http://192.168.0.21:3000",
    "http://192.168.0.21:3000/*",
    "https://login.microsoftonline.com/*",
    "https://localhost:8000",
    "https://localhost:8000/*",
    "https://localhost:3000/*",
    "https://127.0.0.1:3000/*",
    "https://127.0.0.1:3000",
    "https://127.0.0.1:8000/*",
    "https://localhost:8443",
    "https://localhost:8443/*",
    "https://192.168.1.175:8443/*",
    "https://192.168.1.175:8443",
    "https://192.168.1.175:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(mail_router)


@app.on_event("startup")
async def on_startup():
    print("Started")
