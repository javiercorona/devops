from pydantic import BaseModel, Field
from typing import List, Optional

class CICDStep(BaseModel):
    name: str = Field(..., example="Build")
    run: Optional[str] = Field(None, example="pytest")
    uses: Optional[str] = Field(None, example="actions/checkout@v2")

class CICDRequest(BaseModel):
    platform: str = Field(..., example="github")
    steps: List[CICDStep] = Field(
        ...,
        example=[{"name": "Build", "run": "pytest"}]
    )
