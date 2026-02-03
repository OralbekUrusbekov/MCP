from typing import Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None


class QueryResponse(BaseModel):
    response: str
    query: str
    success: bool