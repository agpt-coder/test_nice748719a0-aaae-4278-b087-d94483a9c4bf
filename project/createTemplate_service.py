from datetime import datetime
from typing import Dict

import prisma
import prisma.models
from pydantic import BaseModel


class CreateTemplateResponse(BaseModel):
    """
    Output model for a newly created email template. It returns all the details of the template including id which is automatically generated, title, content, its category, and the date it was created.
    """

    id: str
    title: str
    content: str
    category: str
    createdAt: datetime


async def createTemplate(
    title: str, content: str, metadata: Dict[str, str]
) -> CreateTemplateResponse:
    """
    Creates a new email template. This endpoint accepts JSON-formatted input including template attributes like title, content, and metadata. It would use data validation to ensure required fields are provided before storing. Expected response is the newly created template object with an HTTP 201 status on success.

    Args:
    title (str): The title of the email template which sums up the content.
    content (str): The detailed content of the email template.
    metadata (Dict[str, str]): Optional additional metadata related to the template which might include targeting details or content tags.

    Returns:
    CreateTemplateResponse: Output model for a newly created email template. It returns all the details of the template including id which is automatically generated, title, content, its category, and the date it was created.

    Example:
    template_response = await createTemplate("Monthly Newsletter", "This is the content of the newsletter.", {"urgency": "high"})
    """
    category_guess = "General"
    new_template = await prisma.models.Template.prisma().create(
        data={
            "content": content,
            "category": category_guess,
            "featureId": "appropriate_feature_id",
        }
    )
    return CreateTemplateResponse(
        id=new_template.id,
        title=title,
        content=new_template.content,
        category=new_template.category,
        createdAt=new_template.createdAt,
    )
