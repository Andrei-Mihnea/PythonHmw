from pydantic import BaseModel
from typing import Optional

class MathRequest(BaseModel):
    operation:str # 'power', 'fibonacci', or 'factorial'
    a:int
    b: Optional[int] = None
