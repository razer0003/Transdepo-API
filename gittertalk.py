from typing import Dict, Any
from pydantic import BaseModel

class gittertalk(BaseModel):
    act: str
    obj: str
    params: Dict[str, Any] = {}

def gittertalk_to_string(gt: gittertalk) -> str:
    """
    Converts gittertalk object to a compact string representation.
    """
    base = f"act:{gt.act};obj:{gt.obj}"
    for k, v in gt.params.items():
        base += f";{k}:{v}"
    return base