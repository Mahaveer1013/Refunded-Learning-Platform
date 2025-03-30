from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .core.database import Base, engine
from .routes.auth_routes import router as auth_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Authentication Service"}