from pydantic import BaseModel

class UserScoreResponse(BaseModel):
    score: int