from pydantic import BaseModel, Field

class ReviewAction(BaseModel):
    action: str = Field(
        ...,
        regex=r"^(approve|reject)$",
        description="Action to take on the request",
    )
