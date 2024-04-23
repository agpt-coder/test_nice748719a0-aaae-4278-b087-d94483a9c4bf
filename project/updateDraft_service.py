import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UpdateDraftResponse(BaseModel):
    """
    Model representing the response after attempting to update a draft. It indicates whether the update was successful or not.
    """

    draftId: str
    updated: bool


async def updateDraft(draftId: str, content: str) -> UpdateDraftResponse:
    """
    Updates the content of an existing draft identified by the draftId. It accepts revised content and updates the draft in the database. Used primarily by users in editing roles to refine and finalize drafts.

    Args:
        draftId (str): The unique identifier of the draft to be updated.
        content (str): The new content to update the draft with. This replaces the existing content.

    Returns:
        UpdateDraftResponse: Model representing the response after attempting to update a draft. It indicates whether the update was successful or not.
    """
    draft = await prisma.models.Draft.prisma().find_unique(where={"id": draftId})
    if draft:
        updated_draft = await prisma.models.Draft.prisma().update(
            where={"id": draftId},
            data={"content": content, "status": prisma.enums.DraftStatus.EDITED},
        )
        return UpdateDraftResponse(draftId=draftId, updated=True)
    else:
        return UpdateDraftResponse(draftId=draftId, updated=False)
