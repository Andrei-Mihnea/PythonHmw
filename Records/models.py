from pydantic import BaseModel
from typing import Optional

class MathRequest(BaseModel):
    a:int
    b: Optional[int] = None
