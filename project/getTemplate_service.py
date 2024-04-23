from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class GetTemplateResponse(BaseModel):
    """
    This response model outlines the structure of the data returned for a single email template, directly reflecting the database structure to ensure all relevant details are included.
    """

    id: str
    content: str
    category: str
    createdAt: datetime


async def getTemplate(templateId: str) -> GetTemplateResponse:
    """
    Fetches a specific template by its unique identifier, 'templateId'. The response includes complete details of the template such as title, content, and creation date. Useful for template previews or editing.

    Args:
        templateId (str): Unique identifier of the template to fetch.

    Returns:
        GetTemplateResponse: This response model outlines the structure of the data returned for a single email template, directly reflecting the database structure to ensure all relevant details are included.
    """
    template = await prisma.models.Template.prisma().find_unique(
        where={"id": templateId}
    )
    if not template:
        raise ValueError(f"No template found with ID {templateId}")
    return GetTemplateResponse(
        id=template.id,
        content=template.content,
        category=template.category,
        createdAt=template.createdAt,
    )
