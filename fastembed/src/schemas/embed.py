from typing import List, Union

from pydantic import BaseModel


class Embed(BaseModel):
    provider: str
    model: str
    query: Union[str, List]
