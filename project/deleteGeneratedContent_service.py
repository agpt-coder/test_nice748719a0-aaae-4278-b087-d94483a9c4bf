import prisma
import prisma.models
from pydantic import BaseModel


class DeleteContentResponse(BaseModel):
    """
    Provides confirmation after the successful deletion of the AI-generated content.
    """

    confirmation: str


async def deleteGeneratedContent(contentId: str) -> DeleteContentResponse:
    """
    Deletes a specific generated content. This is crucial for managing data privacy and storage. Returns confirmation of the deletion.

    Args:
        contentId (str): Unique identifier for the draft content to be deleted.

    Returns:
        DeleteContentResponse: Provides confirmation after the successful deletion of the AI-generated content.

    Example:
        # Assuming there's AI-generated content with id 'cj82jbn4300001pfbdxgbnbxz'.
        response = await deleteGeneratedContent('cj82jbn4300001pfbdxgbnbxz')
        print(response.confirmation)
        > 'Content cj82jbn4300001pfbdxgbnbxz successfully deleted.'
    """
    draft = await prisma.models.Draft.prisma().delete(where={"id": contentId})
    if draft:
        return DeleteContentResponse(
            confirmation=f"Content {contentId} successfully deleted."
        )
    else:
        return DeleteContentResponse(
            confirmation="Content not found or already deleted."
        )
