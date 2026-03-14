from pydantic import BaseModel


class ToolCard(BaseModel):
    slug: str
    name: str
    category: str
    description: str
