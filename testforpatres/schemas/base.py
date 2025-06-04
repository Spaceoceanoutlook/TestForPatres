from pydantic import BaseModel
from pydantic import ConfigDict

class BaseResponse(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True) # Автоконвертация из ORM-моделей
