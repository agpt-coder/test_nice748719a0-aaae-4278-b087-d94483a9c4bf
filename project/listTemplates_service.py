import math
from typing import List, Optional

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


class GetTemplatesResponse(BaseModel):
    """
    The response model that returns an array of email templates. Includes pagination details to handle the navigation through the template listings.
    """

    templates: List[Template]
    totalTemplates: int
    currentPage: int
    totalPages: int


async def listTemplates(
    page: int, limit: int, category: Optional[str], sortBy: str
) -> GetTemplatesResponse:
    """
    Retrieves a list of all available email templates. It returns an array of template objects, sorted by the date they were updated. This endpoint supports pagination and filtering parameters to handle large volumes of data.

    Args:
    page (int): Specifies the page number in the pagination of template listings.
    limit (int): Specifies the number of templates to return per page.
    category (Optional[str]): Optional filter to list templates by specific categories.
    sortBy (str): Parameter to specify the sorting order of the templates based on the date updated. Default is 'desc' for descending.

    Returns:
    GetTemplatesResponse: The response model that returns an array of email templates. Includes pagination details to handle the navigation through the template listings.
    """
    query_parameters = {
        "skip": (page - 1) * limit,
        "take": limit,
        "order": {"createdAt": "desc" if sortBy.lower() == "desc" else "asc"},
    }
    if category:
        query_parameters["where"] = {"category": category}
    templates = await prisma.models.Template.prisma().find_many(**query_parameters)
    total_count = await prisma.models.Template.prisma().count(
        where=query_parameters.get("where", {})
    )
    template_objects = [
        Template(
            templateId=template.id,
            title=template.content[:30],
            content=template.content,
            category=template.category,
        )
        for template in templates
    ]
    total_pages = math.ceil(total_count / limit) if limit > 0 else 0
    return GetTemplatesResponse(
        templates=template_objects,
        totalTemplates=total_count,
        currentPage=page,
        totalPages=total_pages,
    )
