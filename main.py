from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from models import Project, Technology, response
from utils.mongodb import MongoDB
from utils.otp_auth import authenticate_otp, unauthorized_msg

load_dotenv()
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


mongodb = MongoDB()
mongodb.resolve_db()

@app.get("/")
async def root():
    """Redirects to the API documentation."""
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


@app.get("/projects")
async def get_all_projects(otp: str = None):
    """Returns a list of all projects."""
    if getenv("AUTH") != "False" and not authenticate_otp(otp):
        return response(**unauthorized_msg)

    return response(
        True,
        "Successfully retrieved all projects.",
        mongodb.find("projects", {"_id": {"$ne": 0}}),
    )


@app.get("/projects/{project_id}")
async def get_project_by_id(project_id: str, otp: str = None):
    """Returns a single project."""
    if getenv("AUTH") != "False" and not authenticate_otp(otp):
        return response(**unauthorized_msg)

    if project := mongodb.find_one("projects", {"id": project_id}):
        return response(True, "Successfully retrieved project.", project)
    else:
        return response(False, "Project not found.")


@app.post("/projects/add")
async def add__project(project: Project, otp: str = None):
    """Adds a new project."""
    if getenv("AUTH") != "False" and not authenticate_otp(otp):
        return response(**unauthorized_msg)

    metadata = mongodb.find_one("projects", {"_id": 0}) or {"_id": 0, "count": 0}
    metadata["count"] += 1
    project.id = f"p{metadata['count']:03}"

    try:
        mongodb.update_one("projects", {"_id": 0}, {"$set": metadata})
    except Exception as e:
        return response(False, "Failed to update metadata.", str(e))

    try:
        mongodb.insert_one("projects", project.model_dump())
        return response(True, "Successfully added project.", project.model_dump())
    except Exception as e:
        metadata["count"] -= 1
        mongodb.update_one("technologies", {"_id": 0}, {"$set": metadata})
        return response(False, "Failed to add project.", str(e))


@app.get("/technologies")
async def get_all_technologies(otp: str = None):
    """Returns a list of all technologies."""
    if getenv("AUTH") != "False" and not authenticate_otp(otp):
        return response(**unauthorized_msg)

    return response(
        True,
        "Successfully retrieved all technologies.",
        mongodb.find("technologies", {"_id": {"$ne": 0}}),
    )


@app.get("/technologies/{technology_id}")
async def get_technology_by_id(technology_id: str, otp: str = None):
    """Returns a single technology."""
    if getenv("AUTH") != "False" and not authenticate_otp(otp):
        return response(**unauthorized_msg)

    if technology := mongodb.find_one("technologies", {"id": technology_id}):
        return response(True, "Successfully retrieved technology.", technology)
    else:
        return response(False, "Technology not found.")


@app.post("/technologies/add")
async def add_technology(technology: Technology, otp: str = None):
    """Adds a new technology."""
    if getenv("AUTH") != "False" and not authenticate_otp(otp):
        return response(**unauthorized_msg)

    metadata = mongodb.find_one("technologies", {"_id": 0}) or {"_id": 0, "count": 0}
    metadata["count"] += 1
    technology.id = f"t{metadata['count']:03}"

    try:
        mongodb.update_one("technologies", {"_id": 0}, {"$set": metadata})
    except Exception as e:
        return response(False, "Failed to update metadata.", str(e))

    try:
        mongodb.insert_one("technologies", technology.model_dump())
        return response(True, "Successfully added technology.", technology)
    except Exception as e:
        print(e)
        metadata["count"] -= 1
        mongodb.update_one("technologies", {"_id": 0}, {"$set": metadata})
        return response(False, "Failed to add technology.", str(e))
