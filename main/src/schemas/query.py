from typing import Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    ext_id: int = None
    query: Optional[str] = None


class QueryResponse(BaseModel):
    ext_id: int
    result: Optional[str] = None
