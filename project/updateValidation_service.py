from typing import Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class QualityCheckUpdateResponse(BaseModel):
    """
    Response model representing the updated state of the validation request.
    """

    success: bool
    updatedValidationId: str
    updatedDetails: Dict[str, str]


async def updateValidation(
    validationId: str,
    newContent: str,
    newModelType: Optional[str],
    additionalNotes: Optional[str],
) -> QualityCheckUpdateResponse:
    """
    Updates the details or parameters of an existing validation request. Useful for adding notes or adjusting the validation parameters after the initial request.

    Args:
        validationId (str): The unique identifier for the validation request to be updated.
        newContent (str): The new content or adjusted parameters for validation.
        newModelType (Optional[str]): Optional updated model type to be used for re-validation.
        additionalNotes (Optional[str]): Additional notes or contextual information added by the administrator during the update.

    Returns:
        QualityCheckUpdateResponse: Response model representing the updated state of the validation request.
    """
    draft = await prisma.models.Draft.prisma().find_unique(where={"id": validationId})
    if draft is None:
        return QualityCheckUpdateResponse(
            success=False,
            updatedValidationId=validationId,
            updatedDetails={"error": "Validation with the provided ID does not exist."},
        )
    update_data = {"content": newContent}
    if newModelType:
        model = await prisma.models.AIModel.prisma().find_first(
            where={"modelType": newModelType}
        )
        if model:
            update_data["modelId"] = model.id
        else:
            return QualityCheckUpdateResponse(
                success=False,
                updatedValidationId=validationId,
                updatedDetails={"error": "Specified model type does not exist."},
            )
    await prisma.models.Draft.prisma().update(
        where={"id": validationId}, data=update_data
    )
    updatedDetails = {
        "newContent": newContent,
        "newModelType": newModelType if newModelType else "Unchanged",
        "additionalNotes": additionalNotes
        if additionalNotes
        else "No additional notes provided",
    }
    if additionalNotes:
        await prisma.models.Edit.prisma().create(
            data={"content": additionalNotes, "draftId": validationId}
        )
    return QualityCheckUpdateResponse(
        success=True, updatedValidationId=validationId, updatedDetails=updatedDetails
    )
