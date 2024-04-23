from enum import Enum
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetModelsRequest(BaseModel):
    """
    This model describes the request for fetching AI models, potentially supporting filtering parameters in future iterations. Currently, it includes no specific parameters as it a basic GET request.
    """

    pass


class ModelType(Enum):
    """
    Enumeration of available AI model types which include GPT_4_TURBO and CUSTOM_CHECKER.
    """

    GPT_4_TURBO: str
    CUSTOM_CHECKER: str


class AIModelDetail(BaseModel):
    """
    Detailed information about an AI model.
    """

    name: str
    description: str
    modelType: ModelType
    availability: bool


class GetModelsResponse(BaseModel):
    """
    Response model containing a list of AI models available for content generation, detailing each model's characteristics.
    """

    models: List[AIModelDetail]


async def listModels(request: GetModelsRequest) -> GetModelsResponse:
    """
    Retrieves a list of available AI models for content generation, including critical details.

    Args:
        request (GetModelsRequest): Request object for fetching AI models.

    Returns:
        GetModelsResponse: Response object containing a list of AI models details.
    """
    models_in_db = await prisma.models.AIModel.prisma().find_many(
        include={"Feature": True}
    )
    models_details = [
        AIModelDetail(
            name=model.Feature.name,
            description=model.Feature.description,
            modelType=ModelType[model.modelType.name],
            availability=True,
        )
        for model in models_in_db
        if model.Feature is not None
    ]
    return GetModelsResponse(models=models_details)
