from pydantic import BaseModel, Field
from typing import List

class ResourceDefinition(BaseModel):
    type: str = Field(..., example="ec2")
    size: str = Field(..., example="t3.micro")

class InfrastructureRequest(BaseModel):
    provider: str = Field(..., example="aws")
    resources: List[ResourceDefinition] = Field(
        ...,
        example=[{"type": "ec2", "size": "t3.micro"}]
    )
