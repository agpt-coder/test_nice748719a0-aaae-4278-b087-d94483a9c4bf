from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ValidationResults(BaseModel):
    """
    Model describing the results from the AI content validation process.
    """

    accuracy: float
    errors: List[str]


class QualityCheckStatusResponse(BaseModel):
    """
    Response model indicating the current status of the content validation process. It includes the status and results if the validation is complete.
    """

    validationStatus: str
    validationResults: Optional[ValidationResults] = None


async def getValidationStatus(validationId: str) -> QualityCheckStatusResponse:
    """
    Retrieves the status of a content validation process by its unique identifier. It returns the current status of the validation and any results if the validation is complete.

    Args:
        validationId (str): The unique identifier for a content validation request, used to retrieve the status.

    Returns:
        QualityCheckStatusResponse: Response model indicating the current status of the content validation process. It includes the status and results if the validation is complete.

    Example:
        # Assuming a suitable validationId is "val123"
        response = await getValidationStatus("val123")
        # Possible output:
        # QualityCheckStatusResponse(validationStatus='FINALIZED', validationResults=ValidationResults(accuracy=0.95, errors=[]))
    """
    draft = await prisma.models.Draft.prisma().find_unique(where={"id": validationId})
    if not draft:
        raise ValueError("No validation process found with the provided validation ID")
    response_data = {"validationStatus": draft.status}
    if draft.status == "FINALIZED":
        last_edit = await prisma.models.Edit.prisma().find_many(
            where={"draftId": validationId}, order={"createdAt": "desc"}, take=1
        )
        errors = [e.content for e in last_edit] if last_edit else []
        validation_results = ValidationResults(accuracy=0.9, errors=errors)
        response_data["validationResults"] = validation_results
    return QualityCheckStatusResponse(**response_data)
