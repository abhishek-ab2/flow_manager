from pydantic import BaseModel

class StartResponse(BaseModel):
    run_id: str
