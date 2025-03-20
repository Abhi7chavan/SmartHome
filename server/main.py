from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from service.models.permission import PermissionBase
from service.models.licence import LicenseBase
from service.models.user import Base
from service.models.submeter import SubmeterBase
from service.models.household import houseitembase
from service.models.database import engine
from service.models.app import app
import os
from pathlib import Path
import importlib

# Call this function during app startup to create the database schema
def create_database():
    Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    PermissionBase.metadata.create_all(bind=engine)
    SubmeterBase.metadata.create_all(bind=engine)
    houseitembase.metadata.create_all(bind=engine)
    LicenseBase.metadata.create_all(bind=engine)
@app.on_event("startup")
async def startup_event():
    create_database()
    print("Server is starting up!")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to the correct origin or set it to ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory path for the 'service' folder
service_dir = Path(__file__).parent / "service"

# Dynamically load all Python files in the 'service' folder
service_files = [f.replace('.py', '') for f in os.listdir(service_dir) if f.endswith('.py') and f != '__init__.py']

# Import and include each router in the main FastAPI application
for service_file in service_files:
    module_path = f'service.{service_file}'
    module = importlib.import_module(module_path)
    app.include_router(module.router)
