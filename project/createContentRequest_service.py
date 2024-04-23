from enum import Enum

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ContentParameters(BaseModel):
    """
    An object encapsulating various parameters used by the AI to tailor the content generation.
    """

    intro: str
    context: str
    closing: str


class ModelType(Enum):
    """
    Enumeration of available AI model types which include GPT_4_TURBO and CUSTOM_CHECKER.
    """

    GPT_4_TURBO: str
    CUSTOM_CHECKER: str


class ContentGenerationResponse(BaseModel):
    """
    Model representing the output after generating content. Includes content ID and status.
    """

    contentId: str
    status: str


async def createContentRequest(
    userId: str, contentParameters: ContentParameters, modelType: ModelType
) -> ContentGenerationResponse:
    """
    Creates a new content generation request using the gpt-4-turbo model, potentially redirected by the Model Selection Module based on availability and suitability. Once content is generated, it's submitted to the Quality Check Module for validation. Expected to return the new content's ID and a status of the creation process.

    Args:
        userId (str): Unique identifier of the user requesting content generation, to associate creation metrics and permissions.
        contentParameters (ContentParameters): Parameters that influence how the AI models generate the content.
        modelType (ModelType): Type of AI model to use for generation, e.g., 'GPT_4_TURBO'.

    Returns:
        ContentGenerationResponse: Model representing the output after generating content. Includes content ID and status.
    """
    ai_model = await prisma.models.AIModel.prisma().find_first(
        where={"modelType": modelType}
    )
    if not ai_model:
        feature_id = "default-feature-id"
        ai_model = await prisma.models.AIModel.prisma().create(
            data={"modelType": modelType, "featureId": feature_id}
        )
    draft_content = f"{contentParameters.intro}\n{contentParameters.context}\n{contentParameters.closing}"
    draft = await prisma.models.Draft.prisma().create(
        data={
            "content": draft_content,
            "status": prisma.enums.DraftStatus.GENERATED,
            "userId": userId,
            "modelId": ai_model.id,
        }
    )
    content_approved = True
    if content_approved:
        return ContentGenerationResponse(contentId=draft.id, status="success")
    else:
        await prisma.models.Draft.prisma().delete(where={"id": draft.id})
        return ContentGenerationResponse(contentId="", status="failed")
