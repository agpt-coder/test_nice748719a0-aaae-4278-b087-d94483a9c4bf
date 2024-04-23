from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class FetchDraftResponse(BaseModel):
    """
    Response model that includes detailed properties of a draft, such as its content, status, and last edited timestamp.
    """

    draftId: str
    content: str
    status: str
    lastEdited: datetime


async def getDraftById(draftId: str) -> FetchDraftResponse:
    """
    Fetches a specific draft by its unique identifier. This route is used to retrieve detailed information
    about a draft to allow for focused editing. Response includes fields like content, status, and last
    edited timestamp. Expected output: {draftId: string, content: string, status: string, lastEdited: timestamp}.

    Args:
        draftId (str): The unique identifier of the draft to be fetched.

    Returns:
        FetchDraftResponse: Response model that includes detailed properties of a draft,
                            such as its content, status, and last edited timestamp.

    Example:
        draft = await getDraftById('abcd1234xyz')
        > FetchDraftResponse(draftId='abcd1234xyz', content='Hello World', status='GENERATED', lastEdited=datetime.now())
    """
    draft = await prisma.models.Draft.prisma().find_unique(where={"id": draftId})
    if draft is None:
        raise ValueError("Draft not found")
    response = FetchDraftResponse(
        draftId=draft.id,
        content=draft.content,
        status=draft.status,
        lastEdited=draft.updatedAt,
    )
    return response
