import prisma
import prisma.models
from pydantic import BaseModel


class DeleteValidationResponse(BaseModel):
    """
    This model confirms the successful deletion of a validation request.
    """

    success: bool
    message: str


async def deleteValidation(validationId: str) -> DeleteValidationResponse:
    """
    Deletes a specific validation request identified by {validationId}. This is typically allowed for users who have the authority to manage or need to clear outdated validation tasks.

    Args:
    validationId (str): The unique identifier for the validation request to be deleted.

    Returns:
    DeleteValidationResponse: This model confirms the successful deletion of a validation request, whether successful or not.
    """
    try:
        result = await prisma.models.Draft.prisma().delete(where={"id": validationId})
        return DeleteValidationResponse(
            success=True, message="Validation successfully deleted."
        )
    except Exception as e:
        return DeleteValidationResponse(success=False, message=str(e))
