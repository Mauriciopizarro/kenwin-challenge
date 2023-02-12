from typing import Optional
from pydantic import Field, BaseModel
from datetime import datetime


class Task(BaseModel):

    status: str
    owner_id: str
    description: str
    difficult: int = Field(None, ge=1, le=10)
    date_created: datetime
    date_finished: Optional[datetime]

    def finish_task(self):
        self.status = "finished"


