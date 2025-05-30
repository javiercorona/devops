import configparser
from pathlib import Path

from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security.api_key import APIKeyHeader, APIKey
from starlette.responses import RedirectResponse
from pydantic import BaseModel, Field

from sources.models.infrastructure import InfrastructureRequest
from sources.models.deployment import CICDRequest
from sources.agents.terraform_agent import TerraformAgent
from sources.agents.cicd_agent import CICDAgent
from sources.agents.devops_agent import DevOpsAgent
from sources.database.db_handler import DBHandler

# Load configuration
config = configparser.ConfigParser()
config.read(Path(__file__).parent / "config.ini")

# API Key from config
API_KEY = config.get("AUTH", "api_key", fallback="change-me")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Depends(api_key_header)) -> APIKey:
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# Initialize FastAPI app
app = FastAPI(
    title="DevOps Automation Assistant",
    version="0.1.0",
    description="Generate Terraform, CI/CD, and other DevOps artifacts via HTTP endpoints",
    dependencies=[Depends(get_api_key)],
)

# Mount static files for a simple UI
app.mount("/static", StaticFiles(directory="static"), name="static")

# Landing page redirects to static index.html
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/static/index.html")

# Routers
infra_router = APIRouter(prefix="/generate/terraform", tags=["Terraform"])
cicd_router  = APIRouter(prefix="/generate/cicd",     tags=["CI/CD"])
devops_router = APIRouter(prefix="/generate",         tags=["DevOps"])

# Agent & DB instances
terraform_agent = TerraformAgent()
cicd_agent      = CICDAgent()
devops_agent    = DevOpsAgent()
db              = DBHandler()

# Terraform endpoint
@infra_router.post("", response_model=dict)
def generate_terraform(req: InfrastructureRequest):
    code = terraform_agent.generate_infrastructure(req)
    return {"code": code}

# CI/CD endpoint
@cicd_router.post("", response_model=dict)
def generate_cicd(req: CICDRequest):
    code = cicd_agent.generate_pipeline(req)
    return {"code": code}

# DevOps composite endpoints
class DockerRequest(BaseModel):
    base_image: str = Field("python:3.9-slim", example="python:3.9-slim")
    port: int       = Field(8000,            example=8000)

@devops_router.post("/dockerfile", response_model=dict)
def generate_dockerfile(req: DockerRequest):
    code = devops_agent.generate_dockerfile(req.base_image, req.port)
    return {"code": code}

class K8sRequest(BaseModel):
    name: str = Field(..., example="my-app")
    image: str = Field(..., example="my-app:latest")
    port: int  = Field(8000,  example=8000)

@devops_router.post("/k8s", response_model=dict)
def generate_k8s(req: K8sRequest):
    code = devops_agent.generate_k8s_deployment(req.name, req.image, req.port)
    return {"code": code}

@devops_router.post("/ansible", response_model=dict)
def generate_ansible():
    code = devops_agent.generate_ansible_playbook()
    return {"code": code}

class CloudFormationRequest(BaseModel):
    stack_name: str = Field(..., example="my-stack")
    resources: list = Field(..., example=[{"name": "MyBucket", "definition": {}}])

@devops_router.post("/cloudformation", response_model=dict)
def generate_cloudformation(req: CloudFormationRequest):
    code = devops_agent.generate_cloudformation(req.stack_name, req.resources)
    return {"code": code}

class MonitoringRequest(BaseModel):
    system: str = Field(..., example="prometheus")
    metrics: list = Field(..., example=[{"job_name": "api", "targets": ["localhost:9090"]}])

@devops_router.post("/monitoring", response_model=dict)
def generate_monitoring(req: MonitoringRequest):
    try:
        code = devops_agent.generate_monitoring_config(req.system, req.metrics)
        return {"code": code}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Persistence Endpoints
@app.post("/artifacts", response_model=dict)
def save_artifact(artifact: dict):
    key = artifact.get("key")
    code = artifact.get("code")
    if not key or not code:
        raise HTTPException(status_code=400, detail="'key' and 'code' are required fields")
    db.save_artifact(key, code)
    return {"status": "saved", "key": key}

@app.get("/artifacts/{key}", response_model=dict)
def get_artifact(key: str):
    code = db.get_artifact(key)
    if code == "":
        raise HTTPException(status_code=404, detail="Artifact not found")
    return {"key": key, "code": code}

@app.get("/artifacts", response_model=dict)
def list_artifacts():
    keys = list(db.store.keys())
    return {"keys": keys}

# Include routers in app
app.include_router(infra_router)
app.include_router(cicd_router)
app.include_router(devops_router)
