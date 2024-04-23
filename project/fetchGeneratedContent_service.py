from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class ModelType(Enum):
    """
    Enumeration of available AI model types which include GPT_4_TURBO and CUSTOM_CHECKER.
    """

    GPT_4_TURBO: str
    CUSTOM_CHECKER: str


class ModelDetails(BaseModel):
    """
    Details about the AI model used for generating the content.
    """

    modelId: str
    modelType: ModelType


class GetAIContentResponse(BaseModel):
    """
    This response model provides the full generated content along with details about the AI model used and the validation status.
    """

    content: str
    modelDetails: ModelDetails
    validationStatus: str


async def fetchGeneratedContent(contentId: str) -> GetAIContentResponse:
    """
    Retrieves the generated content from a prior request, identified by contentId. It outputs the full content if it's been validated by the Quality Check Module,
    along with metadata regarding the used model and validation status.

    Args:
    contentId (str): Unique identifier for the generated content.

    Returns:
    GetAIContentResponse: This response model provides the full generated content along with details about the AI model used and the validation status.
    """
    draft = await prisma.models.Draft.prisma().find_unique(
        where={"id": contentId}, include={"AIModel": True}
    )
    if not draft or not draft.AIModel:
        raise ValueError(
            "No draft or associated AI model found with the given content ID."
        )
    validation_status = (
        "Validated" if draft.status.name == "FINALIZED" else "Pending Validation"
    )
    model_details = ModelDetails(
        modelId=draft.AIModel.id, modelType=ModelType[draft.AIModel.modelType.name]
    )
    response = GetAIContentResponse(
        content=draft.content,
        modelDetails=model_details,
        validationStatus=validation_status,
    )
    return response
