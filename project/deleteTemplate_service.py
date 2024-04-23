import prisma
import prisma.models
from pydantic import BaseModel


class DeleteTemplateResponse(BaseModel):
    """
    Response model for deleting a template. This endpoint does not provide a response body upon successful deletion, hence no fields are necessary in the response model.
    """

    pass


async def deleteTemplate(templateId: str) -> DeleteTemplateResponse:
    """
    Deletes the specified template by its 'templateId'. This is irreversible and typically restricted to high-level roles. On successful deletion, it usually returns HTTP 204 with no content.

    Args:
    templateId (str): The ID of the template to be deleted.

    Returns:
    DeleteTemplateResponse: Response model for deleting a template. This endpoint does not provide a response body upon successful deletion, hence no fields are necessary in the response model.
    """
    delete_result = await prisma.models.Template.prisma().delete(
        where={"id": templateId}
    )
    if delete_result:
        return DeleteTemplateResponse()
    else:
        raise ValueError("Template deletion unsuccessful. Template ID may not exist.")
