import prisma
import prisma.models
from pydantic import BaseModel


class DeleteDraftResponse(BaseModel):
    """
    Response indicating the result of the delete operation on a draft.
    """

    deleted: bool


async def deleteDraft(draftId: str) -> DeleteDraftResponse:
    """
    Deletes a specific draft identified by draftId. This operation is irreversible and used for drafts that are no longer needed or were created in error. Success response indicates whether the draft was successfully deleted. Response: {deleted: boolean}.

    Args:
    draftId (str): The unique identifier of the draft to be deleted.

    Returns:
    DeleteDraftResponse: Response indicating the result of the delete operation on a draft.
    """
    delete_result = await prisma.models.Draft.prisma().delete(where={"id": draftId})
    return DeleteDraftResponse(deleted=delete_result is not None)
