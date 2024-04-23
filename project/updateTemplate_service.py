from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Template(BaseModel):
    """
    Data structuring for a template object, including content, title, and category.
    """

    templateId: str
    title: str
    content: str
    category: Optional[str] = None


class UpdateTemplateResponse(BaseModel):
    """
    Outputs the updated template object reflecting the changes made.
    """

    template: Template


async def updateTemplate(
    templateId: str, title: str, content: str, category: Optional[str] = None
) -> UpdateTemplateResponse:
    """
    Updates an existing email template identified by 'templateId'. This can modify the template's content, title, and other properties.

    Args:
        templateId (str): Unique identifier for the template
        title (str): The new title for the template
        content (str): The new content for the email template
        category (Optional[str]): Optional category change for the template

    Returns:
        UpdateTemplateResponse: Outputs the updated template object reflecting the changes made
    """
    template_record = await prisma.models.Template.prisma().find_unique(
        where={"id": templateId}, include={"Feature": True}
    )
    if not template_record:
        raise ValueError("Template not found")
    updated_fields = {"title": title, "content": content}
    if category is not None:
        updated_fields["category"] = category
    updated_template = await prisma.models.Template.prisma().update(
        where={"id": templateId}, data=updated_fields
    )
    return UpdateTemplateResponse(template=Template(**updated_template.__dict__))
