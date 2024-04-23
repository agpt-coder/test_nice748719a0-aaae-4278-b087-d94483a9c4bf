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


class ModelSelectionResponse(BaseModel):
    """
    Confirmation of the selected AI model including the model name and selection status.
    """

    modelName: str
    selectionStatus: str


async def selectModel(modelIdentifier: ModelType) -> ModelSelectionResponse:
    """
    Allows a user to select a specific AI model for their session of content generation. Sends the chosen model name (e.g., gpt-4-turbo) to the AI Writing Module and stores this preference for future use. The request should include the model identifier. The expected response would confirm the successful selection, including the model name and status.

    Args:
        modelIdentifier (ModelType): The unique identifier of the AI model selected by the user.

    Returns:
        ModelSelectionResponse: Confirmation of the selected AI model including the model name and selection status.
    """
    model_name = modelIdentifier.value
    model = await prisma.models.AIModel.prisma().find_first(
        where={"modelType": modelIdentifier}
    )
    if model is None:
        model = await prisma.models.AIModel.prisma().create(
            data={"modelType": modelIdentifier, "featureId": "DefaultFeatureID"}
        )
    selection_status = "Selection successful" if model else "Selection failed"
    response = ModelSelectionResponse(
        modelName=model_name, selectionStatus=selection_status
    )
    return response
